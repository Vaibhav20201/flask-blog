from flask import Flask,render_template,url_for

app = Flask(__name__)

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


if __name__=='__main__':
    app.run(debug=True)