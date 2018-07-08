#! /usr/bin/env python3.6

from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   request, jsonify)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Documents
from flask_restful import Api


app = Flask(__name__)
app.secret_key = 'Xqanu6dV6RKAMo5U0OmG2tlJpgIKBBgNaaAjlcXoR4RHZyyBTsodc7DmDF9+vKjkPuFevya7LmOgy9hx3WYKBTuzEhd61VQ2J9J'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# engine = create_engine('sqlite:///docs.db')
engine = create_engine('postgresql://testuser:test123@localhost/docs')
Base.metadata.bind = engine
api = Api(app)

session = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/drawinglist")
def drawinglist():
    # doc_list = session.query(Documents).all()
    return render_template("drawinglist.html")


@app.route("/newdocument", methods=['GET', 'POST'])
def newdocument():
    if request.method == 'POST':
        # newDoc = Documents(project=request.form['newproj'],
        #                    doc_name=request.form['newdoc'],
        #                    revision=request.form['rev'])
        # session.add(newDoc)
        # new_title = DocTitles(title_line_1=request.form['tl1'])
        # session.add(new_title)
        # session.commit()
        flash('Document Added.')
        return render_template("newdocument.html")
    else:
        return render_template("newdocument.html")


@app.route("/deldoc/<int:id>", methods=['GET', 'POST'])
def deldoc(id):
    # docToDelete = session.query(Documents).filter_by(doc_id=id).first()
    if request.method == 'GET':
        # session.delete(docToDelete)
        # session.commit()
        # flash('Document deleted.')
        return redirect(url_for('drawinglist'))


@app.route("/editdoc/<int:id>", methods=['GET'])
def editdoc(id):
    # docToEdit = session.query(Documents).filter_by(doc_id=id).first()
    # docToEdit = session.query(DocTitles).filter_by(title_id=id).first()
    if request.method == 'GET':
        return render_template('edit.html')


@app.route("/newdoc", methods=['GET', 'POST'])
def newdoc():
    if request.method == 'POST':
        new_doc = Documents(doc_title=request.form['newtitle'],
                            doc_contents=request.form['newtext'])
        session.add(new_doc)
        session.commit()
        flash('Document Added.')
        return render_template('newdoc.html')
    else:
        return render_template('newdoc.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages-404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)