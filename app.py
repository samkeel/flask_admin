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


@app.route("/drawinglist")
def drawinglist():
    return render_template("drawinglist.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages-404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)