from flask import Flask, render_template, jsonify, request
from database import get_conn, init_db
import os

app = Flask(__name__)
print('debug')

# make sure the db exists even on a fresh clone
init_db()


@app.route("/")
def home():
    return render_template("index.html")


# ---------- api ----------

@app.route("/api/profile")
def api_profile():
    conn = get_conn()
    row = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "db not seeded, run seed_data.py"}), 500
    return jsonify(dict(row))


@app.route("/api/skills")
def api_skills():
    conn = get_conn()
    rows = conn.execute("SELECT category, items FROM skills ORDER BY id").fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({
            "category": r["category"],
            "items": [s.strip() for s in r["items"].split(",")],
        })
    return jsonify(out)


@app.route("/api/projects")
def api_projects():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM projects ORDER BY sort_order").fetchall()
    conn.close()
    out = []
    for r in rows:
        p = dict(r)
        p["stack"] = [s.strip() for s in p["stack"].split(",")]
        p["highlights"] = p["highlights"].split("\n")
        out.append(p)
    return jsonify(out)


@app.route("/api/experience")
def api_experience():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM experience ORDER BY id").fetchall()
    conn.close()
    out = []
    for r in rows:
        e = dict(r)
        e["bullets"] = e["bullets"].split("\n")
        out.append(e)
    return jsonify(out)


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    body = (data.get("message") or "").strip()

    if not body or not email:
        return jsonify({"ok": False, "error": "email and message are required"}), 400
    if len(body) > 2000:
        return jsonify({"ok": False, "error": "message too long"}), 400

    conn = get_conn()
    conn.execute(
        "INSERT INTO messages (sender_name, sender_email, body) VALUES (?,?,?)",
        (name, email, body),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# quick health check, handy when i deploy this somewhere
@app.route("/api/ping")
def ping():
    return jsonify({"status": "up"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
