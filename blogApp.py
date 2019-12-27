from flask import Flask, render_template, url_for, request, redirect

from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/parallax")
def parallax():
    return render_template('parallax.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        username = userDetails['username']
        password = userDetails['password']
        confpassword = userDetails['confpassword']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_signup(name, email, username, password, confpassword) VALUES(%s, %s, %s, %s, %s)",(name, email, username, password, confpassword))
        mysql.connection.commit()
        cur.close()
        return render_template('parallax.html')
    return render_template('parallax.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Me aalo")
    if request.method == 'POST':
        userLoginDetails = request.form
        email = userLoginDetails['email']
        password = userLoginDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from user_signup where email='" + email + "' and password='" + password + "'")
        
        mysql.connection.commit()
        
        data = cur.fetchone()
        print(data[0])
        cur.close()
        return render_template('home.html', userdata= posts)
        

    else:
        return "failed"

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)


