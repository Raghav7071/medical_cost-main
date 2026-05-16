from repositories.db import connect


def save_prediction(user_id: int | None, disease: str, country: str, total_cost: float) -> None:
    if not user_id:
        return
    conn = connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO predictions (user_id, disease, country, total_cost) VALUES (?, ?, ?, ?)",
        (user_id, disease, country, total_cost),
    )
    conn.commit()
    conn.close()


def get_admin_stats() -> dict:
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM predictions")
    total_preds = c.fetchone()[0]

    c.execute("SELECT disease, COUNT(*) as c FROM predictions GROUP BY disease ORDER BY c DESC LIMIT 1")
    top_disease = c.fetchone()

    conn.close()

    return {
        "total_users": total_users,
        "total_predictions": total_preds,
        "top_disease": top_disease[0] if top_disease else "N/A",
    }
