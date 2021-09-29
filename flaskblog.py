from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'This is my Secret Key.'

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
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "a@b.c" and form.password.data == "12345678":
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Credentials! Please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__=='__main__':
    app.run(debug=True)