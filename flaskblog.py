from flask import Flask, render_template, url_for, flash, redirect
from mongoengine import *
from mongoengine import document
from mongoengine.connection import connect
from mongoengine.errors import DoesNotExist, NotUniqueError
from mongoengine.fields import DateTimeField, IntField, LazyReferenceField, ReferenceField, StringField
from mongoengine.queryset.base import CASCADE
from forms import RegisterationForm, LoginForm
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'This is my Secret Key.'

# connect('flaskblog', port=27018)
connect(host="mongodb://127.0.0.1:27018/flaskblog")

class User(document.Document):
    username = StringField(max_length=20, unique=True, required=True)
    email = StringField(max_length=120, unique=True, required=True)
    image_file = StringField(max_length=20, required=True, default='default.jpg')
    password = StringField(max_length=60, required=True)

    def __repr__(self):
        return f"User('{ self.username }', { self.email }', { self.image_file }')"

class Post(document.Document):
    title = StringField(max_length=100, required=True)
    date_posted = DateTimeField(required=True, default=datetime.utcnow)
    content = StringField(required=True)
    author = ReferenceField('User', reverse_delete_rule=CASCADE, required=True)

    def __repr__(self):
        return f"User('{ self.title }', '{ self.date_posted }')"


posts=[
    {
        'author' : 'Vaibhav Khanna',
        'title' : 'Blog 1',
        'content' : 'Content 1',
        'date_posted' : 'September 29, 2021'
    },
    {
        'author' : 'Vaibhav Khanna',
        'title' : 'Blog 2',
        'content' : 'Content 2',
        'date_posted' : 'September 29, 2021'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=Post.objects.all())

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        try:
            user.save()
            flash(f'Account created for { form.username.data }!', 'success')
            return redirect(url_for('home'))
        except NotUniqueError:
            flash(f'Username or email not unique!', 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user=User.objects(email=form.email.data).get()
            if form.password.data == user.password:
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Email and Password do not match!', 'danger')
        except DoesNotExist:
            flash('This Email is not registered!', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__=='__main__':
    app.run(debug=True)