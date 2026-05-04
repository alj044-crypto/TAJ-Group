from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "devices.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            template_name TEXT NOT NULL,
            command TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("htmlApp.html")


@app.route("/api/templates", methods=["GET"])
def get_templates():
    conn = get_db_connection()
    templates = conn.execute("SELECT * FROM templates").fetchall()
    conn.close()

    return jsonify([dict(row) for row in templates])


@app.route("/api/templates", methods=["POST"])
def add_template():
    data = request.get_json()

    device_name = data.get("deviceName")
    template_name = data.get("templateName")
    command = data.get("command")

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO templates (device_name, template_name, command)
        VALUES (?, ?, ?)
    """, (device_name, template_name, command))

    conn.commit()
    conn.close()

    return jsonify({"message": "Template saved successfully"})


@app.route("/api/templates/<int:template_id>", methods=["DELETE"])
def delete_template(template_id):
    conn = get_db_connection()

    conn.execute("DELETE FROM templates WHERE id = ?", (template_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Template deleted"})


if __name__ == "__main__":
    create_tables()
    app.run(debug=True, host= "0.0.0.0", port= 5001) 