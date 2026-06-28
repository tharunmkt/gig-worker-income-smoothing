from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from db import get_connection
from financial_engine import calculate_smoothing
from ai_recommender import (
    generate_ai_insights,
    generate_ai_alerts
)

from payment import create_payment_order
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

app = Flask(__name__)
app.secret_key = "gigworker_secret_2026"


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM accounts WHERE email=%s",
            (email,)
        )

        existing = cur.fetchone()

        if existing:

            flash("Email already registered.")

            cur.close()
            conn.close()

            return redirect("/register")

        hashed = generate_password_hash(password)

        cur.execute("""
            INSERT INTO accounts
            (
                username,
                email,
                password
            )
            VALUES(%s,%s,%s)
        """, (
            username,
            email,
            hashed
        ))

        conn.commit()

        cur.close()
        conn.close()

        flash("Registration Successful.")

        return redirect("/login")

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                username,
                password
            FROM accounts
            WHERE email=%s
        """, (email,))

        account = cur.fetchone()

        cur.close()
        conn.close()

        if account:

            if check_password_hash(account[2], password):

                session["account_id"] = account[0]
                session["username"] = account[1]

                return redirect("/")

        flash("Invalid Email or Password")

        return redirect("/login")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# =========================
# DASHBOARD
# =========================
@app.route("/")
def dashboard():

    if "account_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM users")
    total_workers = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM income_events
        WHERE income_date = CURRENT_DATE
    """)
    actual_income = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(SUM(smoothed_income),0)
        FROM income_events
        WHERE income_date = CURRENT_DATE
    """)
    virtual_salary = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(SUM(current_buffer),0)
        FROM users
    """)
    total_buffer = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(AVG(target_income),0)
        FROM users
    """)
    avg_target = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(AVG(health_score),100)
        FROM users
    """)
    health_score = round(cur.fetchone()[0])

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_workers=total_workers,
        actual_income=actual_income,
        virtual_salary=virtual_salary,
        total_buffer=total_buffer,
        avg_target=avg_target,
        health_score=health_score
    )


# =========================
# WORKERS
# =========================
@app.route("/workers")
def workers():

    if "account_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users ORDER BY id")
    workers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("workers.html", workers=workers)


# =========================
# ADD WORKER
# =========================
@app.route("/add_worker", methods=["GET", "POST"])
def add_worker():

    if "account_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        platform = request.form["platform"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users(name, email, phone, platform)
            VALUES (%s, %s, %s, %s)
        """, (name, email, phone, platform))

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/workers")

    return render_template("add_worker.html")


# =========================
# INCOME
# =========================
@app.route("/income", methods=["GET", "POST"])
def income():

    if "account_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        user_id = request.form["user_id"]
        amount = float(request.form["amount"])
        income_date = request.form["income_date"]

        cur.execute("""
            SELECT target_income, current_buffer
            FROM users
            WHERE id = %s
        """, (user_id,))

        worker = cur.fetchone()

        if not worker:
            cur.close()
            conn.close()
            return "Worker not found", 404

        target_income = float(worker[0])
        current_buffer = float(worker[1])

        result = calculate_smoothing(
            amount,
            target_income,
            current_buffer
        )

        cur.execute("""
            UPDATE users
            SET current_buffer = %s
            WHERE id = %s
        """, (result["new_buffer"], user_id))

        cur.execute("""
            INSERT INTO income_events(
                user_id,
                amount,
                smoothed_income,
                income_date
            )
            VALUES (%s, %s, %s, %s)
        """, (
            user_id,
            amount,
            result["virtual_salary"],
            income_date
        ))

        cur.execute("""
            INSERT INTO buffer_ledger(
                user_id,
                transaction_type,
                amount,
                balance
            )
            VALUES (%s, %s, %s, %s)
        """, (
            user_id,
            result["transaction_type"],
            result["buffer_change"],
            result["new_buffer"]
        ))

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/income")

        # =========================
    # Load workers for dropdown
    # =========================
    cur.execute("SELECT id, name FROM users ORDER BY name")
    workers = cur.fetchall()

    # =========================
    # Load income history
    # =========================
    cur.execute("""
        SELECT
            income_events.user_id,
            users.name,
            income_events.amount,
            income_events.smoothed_income,
            income_events.income_date
        FROM income_events
        JOIN users
            ON users.id = income_events.user_id
        ORDER BY income_events.income_date DESC,
                 income_events.id DESC
    """)

    incomes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "income.html",
        workers=workers,
        incomes=incomes
    )
   
# =========================
# PAY WORKER
# =========================
@app.route("/pay/<int:user_id>")
def pay(user_id):

    if "account_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            users.name,
            income_events.smoothed_income
        FROM income_events
        JOIN users
        ON users.id = income_events.user_id
        WHERE users.id=%s
        ORDER BY income_events.income_date DESC
        LIMIT 1
    """,(user_id,))

    worker = cur.fetchone()

    if worker is None:

        cur.close()
        conn.close()

        flash("No income records found.")

        return redirect("/income")

    worker_name = worker[0]
    amount = float(worker[1])

    order = create_payment_order(amount)

    cur.execute("""
        INSERT INTO payments(
            user_id,
            amount,
            payment_status,
            razorpay_order_id
        )
        VALUES(%s,%s,%s,%s)
    """,
    (
        user_id,
        amount,
        "Pending",
        order["id"]
    ))

    conn.commit()

    cur.close()
    conn.close()

    return render_template(
        "payment.html",
        worker_name=worker_name,
        amount=amount,
        order=order,
        razorpay_key=RAZORPAY_KEY_ID
    )
    
# =========================
# PAYMENT SUCCESS
# =========================   
@app.route("/payment_success")
def payment_success():

    payment_id = request.args.get("payment_id")
    order_id = request.args.get("order_id")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE payments
        SET
            payment_status='Success',
            razorpay_payment_id=%s
        WHERE razorpay_order_id=%s
    """,
    (
        payment_id,
        order_id
    ))

    conn.commit()

    cur.close()
    conn.close()

    flash("Payment Successful!")

    return redirect("/income")

# =========================
# ANALYTICS (AI + CHARTS FIXED)
# =========================
@app.route("/analytics")
def analytics():

    if "account_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()

    # -------------------------
    # BASE METRICS
    # -------------------------
    cur.execute("SELECT COALESCE(SUM(amount),0) FROM income_events")
    total_income = float(cur.fetchone()[0])

    cur.execute("SELECT COALESCE(SUM(smoothed_income),0) FROM income_events")
    total_virtual = float(cur.fetchone()[0])

    cur.execute("SELECT COALESCE(SUM(current_buffer),0) FROM users")
    total_buffer = float(cur.fetchone()[0])

    cur.execute("""
        SELECT platform, COUNT(*)
        FROM users
        GROUP BY platform
    """)
    platforms = cur.fetchall()
    platform_names = [p[0] for p in platforms]
    platform_counts = [p[1] for p in platforms]

    cur.execute("""
        SELECT users.name,
               income_events.amount,
               income_events.smoothed_income,
               income_events.income_date
        FROM income_events
        JOIN users ON users.id = income_events.user_id
        ORDER BY income_events.income_date DESC
        LIMIT 10
    """)
    recent = cur.fetchall()

    # -------------------------
    # AI INPUT
    # -------------------------
    cur.execute("""
        SELECT amount
        FROM income_events
        ORDER BY income_date DESC
        LIMIT 30
    """)
    income_list = [row[0] for row in cur.fetchall()]

    cur.execute("""
        SELECT COALESCE(AVG(target_income),0)
        FROM users
    """)
    avg_target_income = float(cur.fetchone()[0])

    # -------------------------
    # AI PROCESSING
    # -------------------------
    ai_report = generate_ai_insights(
        income_list,
        total_buffer,
        avg_target_income
    )

    alerts = generate_ai_alerts(
        ai_report["health_score"],
        ai_report["stability_index"],
        ai_report["risk_level"],
        total_buffer,
        avg_target_income
    )

    # -------------------------
    # CHART DATA
    # -------------------------
    cur.execute("""
        SELECT amount, income_date
        FROM income_events
        ORDER BY income_date ASC
        LIMIT 30
    """)
    chart_rows = cur.fetchall()

    chart_labels = [str(row[1]) for row in chart_rows]
    chart_values = [float(row[0]) for row in chart_rows]

    cur.close()
    conn.close()

    return render_template(
        "analytics.html",
        total_income=total_income,
        total_virtual=total_virtual,
        total_buffer=total_buffer,
        platform_names=platform_names,
        platform_counts=platform_counts,
        recent=recent,
        ai_report=ai_report,
        alerts=alerts,
        chart_labels=chart_labels,
        chart_values=chart_values
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
    