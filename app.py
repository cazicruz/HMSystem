from flask import Flask, render_template, request, session, redirect, url_for,flash
from  flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from flask_bcrypt import Bcrypt



app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = "hardtoguessstring"
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']= \
 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


bootstrap= Bootstrap(app)
moment = Moment(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------models class definitions
class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True,index=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Roles(db.Model):
    __tablename__= 'roles'
    id= db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(60),unique=True)
    users = db.relationship('User', backref='roles')


# ----------wtf form definition
class LoginForm(FlaskForm):
    username = StringField(' Username: ', validators=[InputRequired()], render_kw={"placeholder": "username"})
    password = PasswordField(' Password: ',validators=[DataRequired(message='Required'), Length(10)], render_kw={"placeholder": "password"})
    loginButton = SubmitField('Login')

class SignUpForm(FlaskForm):
    fname = StringField('firstname', validators=[DataRequired()],  render_kw={"placeholder": "first name"})
    lname = StringField('lastname', validators=[DataRequired()], render_kw={"placeholder": "last name"})
    email = EmailField('email', validators=[InputRequired()],  render_kw={"placeholder": "Email"})
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "pick a username"})
    password1 = PasswordField(U' Password: ',validators=[InputRequired(message='Required'), Length(10)])
    password2 = PasswordField(U'Confirm Password: ',validators=[InputRequired(message='Required'), Length(10), EqualTo('password1')])
    roleSelection = SelectField('Type of user', choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')], validators=[InputRequired(message='select a role')])
    submit = SubmitField('submit')

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError('username exists already.')




# ---------- routing (view functions)


@app.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def home (id):
    user=db.get_or_404(User, id)
    username=user.username

    patient_no= Roles.query.filter_by(title='Patient').count()
    return render_template("home.html",patient_no=patient_no,username=username)

@app.route('/login', methods=['GET','POST'])
def login():
    username = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home', id=user.id))
            
        else:
            flash('username or password incorrect')
            

    return render_template('login.html', form=form)

@app.route('/sign-up',methods=['GET','POST'])
def sign_up():
    form=SignUpForm()
    if form.validate_on_submit():
        role= Roles.query.filter_by(title=form.roleSelection.data).first()
        if role is None:
            role = Roles(title=form.roleSelection.data)
            db.session.add(role)
            db.session.commit()           
            
            
        # -----arranging the form data into variables for easy and neat passing to models
        fname = form.fname.data
        lname = form.lname.data
        mail = form.email.data
        u_name = form.username.data
        pword = bcrypt.generate_password_hash(form.password2.data)
        

        user = User(username=u_name,firstname=fname,lastname=lname,email=mail,password=pword,roles=role)
        db.session.add(user)
        db.session.commit()
        flash('account created')
        return redirect(url_for('login'))
    return render_template('sign-up.html',form=form)




 # error handling creating the custom 500 error page
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#--------- making the app run as a package
if __name__ == '__main__' :
    app.run(debug=True)