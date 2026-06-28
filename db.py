import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="gig_worker_db",
        user="postgres",
        password=130104,
        port="5432"
    )