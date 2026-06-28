import numpy as np

# =====================================================
# CORE METRICS ENGINE
# =====================================================

def compute_metrics(income_list, total_buffer, avg_target_income):

    income_array = np.array(income_list, dtype=float)

    avg_income = np.mean(income_array)
    std_income = np.std(income_array)

    # Stability
    if avg_income == 0:
        stability_index = 0
    else:
        stability_index = 1 - (std_income / avg_income)

    stability_index = max(0, min(1, stability_index))

    # Health
    if avg_target_income == 0:
        health_score = 0
    else:
        health_score = (total_buffer / avg_target_income) * 100

    health_score = max(0, min(100, health_score))

    # Risk
    if health_score < 30:
        risk_level = "Critical"
    elif health_score < 60:
        risk_level = "Moderate Risk"
    elif health_score < 80:
        risk_level = "Stable"
    else:
        risk_level = "Excellent"

    return health_score, stability_index, risk_level


# =====================================================
# INSIGHTS ENGINE
# =====================================================

def generate_ai_insights(income_list, total_buffer, avg_target_income):

    if not income_list:
        return {
            "health_score": 0,
            "stability_index": 0,
            "risk_level": "No Data",
            "insights": ["Not enough data for analysis"]
        }

    health_score, stability_index, risk_level = compute_metrics(
        income_list, total_buffer, avg_target_income
    )

    insights = []

    # Stability insights
    if stability_index < 0.4:
        insights.append("Income is highly unstable. Diversify platforms.")
    elif stability_index < 0.7:
        insights.append("Moderate fluctuations detected.")
    else:
        insights.append("Income is stable.")

    # Buffer insights
    if total_buffer < avg_target_income * 0.3:
        insights.append("Low buffer. Increase savings urgently.")
    elif total_buffer < avg_target_income * 0.7:
        insights.append("Buffer is moderate.")
    else:
        insights.append("Healthy buffer maintained.")

    # Risk insights
    if risk_level == "Critical":
        insights.append("Urgent action required.")
    elif risk_level == "Moderate Risk":
        insights.append("Improve consistency.")
    elif risk_level == "Excellent":
        insights.append("Financial health is strong.")

    return {
        "health_score": round(health_score, 2),
        "stability_index": round(stability_index, 2),
        "risk_level": risk_level,
        "insights": insights
    }


# =====================================================
# ALERT ENGINE
# =====================================================

def generate_ai_alerts(health_score, stability_index, risk_level, total_buffer, avg_target_income):

    alerts = []

    if risk_level == "Critical":
        alerts.append({"type": "danger", "message": "Critical financial risk detected"})

    if health_score < 30:
        alerts.append({"type": "danger", "message": "Health score critically low"})
    elif health_score < 60:
        alerts.append({"type": "warning", "message": "Financial health below safe level"})

    if stability_index < 0.4:
        alerts.append({"type": "warning", "message": "Income unstable"})

    if total_buffer < avg_target_income * 0.3:
        alerts.append({"type": "danger", "message": "Emergency buffer too low"})
    elif total_buffer < avg_target_income * 0.7:
        alerts.append({"type": "warning", "message": "Buffer not safe yet"})

    if health_score > 80 and stability_index > 0.7:
        alerts.append({"type": "success", "message": "System is financially healthy"})

    return alerts


# =====================================================
# 🔮 PREDICTION ENGINE (NEW - STEP 5)
# =====================================================

def predict_income_trend(income_list):

    if len(income_list) < 3:
        return {
            "trend": "Insufficient Data",
            "forecast": []
        }

    recent = income_list[-7:] if len(income_list) >= 7 else income_list

    avg = np.mean(recent)

    # trend direction
    if recent[-1] > recent[0]:
        trend = "Increasing"
    elif recent[-1] < recent[0]:
        trend = "Decreasing"
    else:
        trend = "Stable"

    # simple forecast model (baseline projection)
    forecast = [
        round(avg * (1 + (i * 0.02)), 2)
        for i in range(7)
    ]

    return {
        "trend": trend,
        "forecast": forecast
    }