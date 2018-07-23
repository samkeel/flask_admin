#! /usr/bin/env python3.6
from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   request, jsonify, abort)

from flask_login import (LoginManager,
                         login_required,
                         login_user,
                         logout_user)
from flask_wtf import FlaskForm
from urllib.parse import urlparse, urljoin
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Documents, User
from user import dbUser


app = Flask(__name__)
app.secret_key = 'Xqanu6dV6RKAMo5U0OmG2tlJpgIKBBgNaaAjlcXoR4RHZyyBTsodc7DmDF9+vKjkPuFevya7LmOgy9hx3WYKBTuzEhd61VQ2J9J'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine('postgresql://testuser:test123@localhost/docs')
Base.metadata.bind = engine
login_manager = LoginManager(app)

session = scoped_session(sessionmaker(bind=engine))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


@login_manager.user_loader
def load_user(user_id):
    user = session.query(User).get(user_id)
    if user:
        return dbUser(user)
    else:
        return None

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/", methods=['GET', 'POST'])
def home():
    next = get_redirect_target()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = session.query(User).filter_by(username=username, email=email).first()
        if user:
            if login_user(dbUser(user)):
                return redirect_back('dashboard')
        return render_template('home.html', next=next)
    else:
        return render_template("home.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/drawinglist")
@login_required
def drawinglist():
    # doc_list = session.query(Documents).all()
    return render_template("drawinglist.html")


@app.route("/newdocument", methods=['GET', 'POST'])
@login_required
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
@login_required
def deldoc(id):
    # docToDelete = session.query(Documents).filter_by(doc_id=id).first()
    if request.method == 'GET':
        # session.delete(docToDelete)
        # session.commit()
        # flash('Document deleted.')
        return redirect(url_for('drawinglist'))


@app.route("/editdoc/<int:id>", methods=['GET'])
@login_required
def editdoc(id):
    # docToEdit = session.query(Documents).filter_by(doc_id=id).first()
    # docToEdit = session.query(DocTitles).filter_by(title_id=id).first()
    if request.method == 'GET':
        return render_template('edit.html')


@app.route("/newdoc", methods=['GET', 'POST'])
@login_required
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