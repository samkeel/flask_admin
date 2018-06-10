from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   request)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/main")
def main():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)