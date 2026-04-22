from flask import Flask, render_template
app = Flask("First App")
@app.route("/")
def home():
    return "Hello World"
if __name__ == "__main__":
    app.run(debug=True)





