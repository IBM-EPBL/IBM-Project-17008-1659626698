from flask import Flask, render_template, url_for, redirect, flash
from flask_login import login_user, LoginManager, login_required, logout_user
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
import ibm_db

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'B7-1A3E'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hcq89801;PWD=usAygURNqa4m1FSR", '', '')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    stmt = ibm_db.prepare(conn, 'SELECT * FROM user WHERE id=?')
    ibm_db.bind_param(stmt, 1, user_id)
    ibm_db.execute(stmt)
    user = ibm_db.fetch_tuple(stmt)
    usr_obj = User(user[0], user[1], user[2])
    return usr_obj

class User:
    def __init__(self, id, email, username):
        self.id = id
        self.username = username
        self.email = email

    def to_json(self):
        return {"username": self.username, "email": self.email}
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder":"Email"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    rollnumber = StringField(validators=[InputRequired(), Length(min=5, max=10)], render_kw={"placeholder":"RollNumber"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)],render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        stmt = ibm_db.prepare(conn, 'SELECT * FROM user WHERE username=?')
        ibm_db.bind_param(stmt, 1, username.data)
        ibm_db.execute(stmt)
        existing_user_username = ibm_db.fetch_tuple(stmt)
        if existing_user_username:
            raise ValidationError('That username already exists. Try another one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        stmt = ibm_db.prepare(conn, 'INSERT INTO user (email, username, roll_number, pass_word) VALUES (?, ?, ?, ?)')
        ibm_db.bind_param(stmt, 1, form.email.data)
        ibm_db.bind_param(stmt, 2, form.username.data)
        ibm_db.bind_param(stmt, 3, form.rollnumber.data)
        ibm_db.bind_param(stmt, 4, hashed_password)
        ibm_db.execute(stmt)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        stmt = ibm_db.prepare(conn, 'SELECT * FROM user WHERE username=?')
        ibm_db.bind_param(stmt, 1, form.username.data)
        ibm_db.execute(stmt)
        user = ibm_db.fetch_tuple(stmt)
        if user:
            if bcrypt.check_password_hash(user[4], form.password.data):
                usr_obj = User(user[0], user[1], user[2])
                login_user(usr_obj)
                return redirect(url_for('welcome'))
            else:
                print('Hi')
                flash(f'Invalid credentials, check and try logging in again.', 'danger')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    return render_template('welcome.html')


if __name__ == "__main__":
    app.run(debug=True)
