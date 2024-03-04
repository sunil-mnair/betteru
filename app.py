
import os,re,json
from urllib.request import urlopen
from flask import Flask,render_template,request, redirect,url_for,Response,jsonify,flash,send_file,session

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager,login_required, login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField

app = Flask(__name__, static_url_path='/static')

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "sample.db"))

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# engine = create_engine("sqlite:///{}".format(os.path.join(project_dir, "sample.db")), echo=True)

# Base.metadata.create_all(engine)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from models import *
from forms import *

@login_manager.user_loader
def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

admin = Admin(app,index_view=MainAdminIndexView(),template_mode='bootstrap3')
admin.add_view(AllModelView(User,db.session))

@app.route('/login',methods=['GET','POST'])
def login():
        
    title = "Login"
    
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again.')
            return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user,remember=form.remember.data)
        return redirect(url_for('index'))
    
    return render_template('login.html',title = title,form=form)

@app.route('/signup')
def signup():
    title = "website"
    form = SignupForm()
    return render_template('signup.html',form=form)

@app.route('/signup',methods=['POST'])
def signup_post():
    
    form = SignupForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Username already exists')
            return redirect(url_for('signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(username=form.username.data, password=generate_password_hash(form.password.data))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # code to validate and add user to database goes here
        return redirect(url_for('login'))

    return render_template(url_for('signup'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/',methods=['GET','POST'])
def index():

    return render_template("index.html")
@app.route('/blog',methods=['GET','POST'])
def blog():

    return render_template("blog.html")

@app.route('/recipes',methods=['GET','POST'])
def recipes():
    # url="http://api.edamam.com/api/recipes/v2?type=public&app_id=77494cab&app_key=%20234bf5bb0a16d77da6c4abdc6fd1045f&diet=balanced"
    # recipes=urlopen(url)
    # recipe_list=json.loads(recipes.read())
    # print(recipe_list)
    return render_template("recipes.html")

@app.route('/sleeptracker',methods=['GET','POST'])
def sleeptracker():

    return render_template("sleeptracker.html",name=current_user.username)

@app.route('/workout',methods=['GET','POST'])
def workout():

    return render_template("workout.html",name=current_user.username)

@app.route('/moodtracker',methods=['GET','POST'])
def moodtracker():

    return render_template("moodtracker.html",name=current_user.username)

@app.route('/todolist',methods=['GET','POST'])
def todolist():

    return render_template("todolist.html",name=current_user.username)