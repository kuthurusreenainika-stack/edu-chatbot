
from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import re

app = Flask(__name__, static_folder="static", static_url_path="/static")
DB_PATH = "campus.db"


def search_database(user_text):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    words = set(re.findall(r"\w{3,}", user_text.lower()))
    schema = {
        "schedules": ["building", "room", "event", "day"],
        "dining": ["location", "menu", "notes"],
        "library": ["service", "notes", "hours"],
        "admin": ["topic", "description"]
    }
    results = []
    for table, cols in schema.items():
        where_clauses = []
        params = []
        for col in cols:
            for w in words:
                where_clauses.append(f"{col} LIKE ?")
                params.append(f"%{w}%")
        if where_clauses:
            q = f"SELECT * FROM {table} WHERE " + " OR ".join(where_clauses)
            cur.execute(q, params)
            rows = [dict(r) for r in cur.fetchall()]
            if rows:
                results.append({"table": table, "rows": rows})
    conn.close()
    return results


@app.route("/api/query", methods=["POST"])
def api_query():
    data = request.json or {}
    user_text = data.get("message", "").strip()
    if not user_text:
        return jsonify({"error": "Empty message"}), 400

    db_hits = search_database(user_text)

    if db_hits:
        reply = "Here is what I found:\n"
        for section in db_hits:
            reply += f"\n🔹 {section['table'].capitalize()}:\n"
            for row in section["rows"]:
                reply += "  - " + \
                    ", ".join(f"{k}: {v}" for k, v in row.items()
                              if k != "id") + "\n"
    else:
        reply = "Sorry, I couldn't find anything in the database for your query."

    return jsonify({"reply": reply, "db_hits": db_hits})


@app.route("/")
def root():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
