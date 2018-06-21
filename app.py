#! /usr/bin/env python3.6

from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   request)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Documents
from flask_restful import Api
from stats import Stats

app = Flask(__name__)
app.secret_key = 'Xqanu6dV6RKAMo5U0OmG2tlJpgIKBBgNaaAjlcXoR4RHZyyBTsodc7DmDF9+vKjkPuFevya7LmOgy9hx3WYKBTuzEhd61VQ2J9J'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine('sqlite:///docs.db')
Base.metadata.bind = engine
api = Api(app)

api.add_resource(Stats, '/doccount')

session = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    docCount = session.query(Documents).count()
    return render_template("dashboard.html", docCount=docCount)


@app.route("/drawinglist")
def drawinglist():
    doc_list = session.query(Documents).all()
    docCount = session.query(Documents).count()
    return render_template("drawinglist.html", doc_list=doc_list, docCount=docCount)


@app.route("/newdocument", methods=['GET', 'POST'])
def newdocument():
    if request.method == 'POST':
        newDoc = Documents(project=request.form['newproj'],
                           doc_name=request.form['newdoc'])
        session.add(newDoc)
        session.commit()
        docCount = session.query(Documents).count()
        return render_template("newdocument.html", docCount=docCount)
    else:
        docCount = session.query(Documents).count()
        return render_template("newdocument.html", docCount=docCount)


@app.route("/deldoc/<int:id>", methods=['GET','POST'])
def deldoc(id):
    docToDelete = session.query(Documents).filter_by(doc_id=id).first()
    if request.method == 'GET':
        session.delete(docToDelete)
        session.commit()
        return redirect(url_for('drawinglist'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages-404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)