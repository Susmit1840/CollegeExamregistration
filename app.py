# from crypt import methods
from xml.sax.handler import DTDHandler
from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql
import re


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'cairocoders-ednalan'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testingdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# http://localhost:5000/pythonlogin/ - this will be the login page


@app.route('/', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

    # If account exists in accounts table in out database
        if account:
            print(account)
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            # return 'Logged in successfully!'
            return render_template('home.html',id=account.get('id'),username=account.get('fullname'),gmail=account.get('email'),)
        elif cursor.execute('SELECT * FROM admin1 WHERE username = %s AND password = %s', (username, password)):
            account = cursor.fetchone()
            session['loggedin'] = True
            session['username'] = account['username']
            return render_template('dashboard.html', msg=msg)

        else:    # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)

# http://localhost:5000/register - this will be the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

  # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts(`fullname`, `username`, `password`, `email`) VALUES (%s, %s, %s, %s)',(fullname, username, password, email))
            conn.commit()

            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html',msg=msg)




@app.route('/h')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:

        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'], id=session['id'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))




@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))



@app.route('/profile')
def profile():
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/personal', methods=['GET', 'POST'])
def personal():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
        
    if 'loggedin' in session:
        if request.method == 'POST':
            

            fullname = request.form['name']
            dob = request.form['dob']
            gender = request.form['gender']
            phoneno = request.form['phoneno']
            address = request.form['address']
            emailid = request.form['emailid']
            department = request.form['department']
            year = request.form['year']
            semester = request.form['semester']
            user_id = request.form['user_id']

            
        # Fetch one record and return result
           
           
            # a="INSERT INTO `personal_details`( `DOB`, `Gender`, `contact`, `address`, `email`, `department`, `year`, `semester`) VALUES ",dob,gender,phoneno,address,emailid,department,year,semester
            # a="INSERT INTO `personal_details`(`Name`, `DOB`, `Gender`, `contact`, `address`, `email`, `department`, `year`, `semester`, `user_id`) VALUES ('$fullname','$dob','$gender','$phoneno','$address','$emailid','$department','$year','$semester','$user_id')"
            cursor.execute("INSERT INTO personal_details(Name,DOB,Gender,contact,address,email,department,year,semester,user_id) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",
                           (fullname, dob, gender, phoneno, address, emailid, department, year, semester, user_id))
            # cursor.execute(a)
            conn.commit()
            conn.close()

    return render_template('personal_details.html', username=session['username'], id=session['id'])


@app.route('/exam', methods=['GET', 'POST'])
def exam():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

        #    name = request.form['name']
        #    branch1 = request.form['branch']
        #    semester1 = request.form['semester']
        #    user_id = request.form['user_id']
        username = session['username']

        user_id = session['id']

        cursor.execute(
            "INSERT INTO exam_form(`Name`,`id_r`) VALUES (%s,%s)", (username, user_id))
        # User is loggedin show them the home page
        conn.commit()
        conn.close()
    return render_template('exam_form1.html', username=session['username'], id=session['id'])


@app.route('/result')
def result():
    if 'loggedin' in session:

        return render_template('result_student.html', username=session['username'])


@app.route('/dashboarda')
def dashboarda():
    table_li = []
    conn= mysql.connect()
    cursor =conn.cursor(pymysql.cursors.DictCursor)
    
    if 'loggedin' in session:
     cursor.execute('SELECT * FROM accounts ')
    d = cursor.fetchall()
    for dict in d:
            table_li.append(list(dict.values()))
    conn.close()
    print(table_li)
    return render_template('dashboard.html',d=table_li)

        # return render_template('dashboard.html', username=session['username'])


@app.route('/examinationa')
def examniationa():
    table_li = []
    conn= mysql.connect()
    cursor =conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        # cursor.execute('SELECT * FROM exam_form')
        cursor.execute('SELECT `Name`, `Branch`, `Semester`, `id_r`, `datetime` FROM `exam_form` WHERE 1')
        d = cursor.fetchall()
        for dict in d:
            table_li.append(list(dict.values()))
        conn.close()
        print(table_li)
        return render_template('eg.html',d=table_li)


@app.route('/resulta')
def resulta():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        if request.method =='POST':
            Subj1 = request.form['Subj1']
            Subj2 = request.form['Subj2']
            Subj3 = request.form['Subj3']
            Subj4 = request.form['Subj4']
            Subj5 = request.form['Subj5']
            rl = request.form['rl']
            print(Subj1)
            cursor.execute("INSERT INTO result(`Mathematics`,`Physics`,`Chemistry`,`Engineering Mechanics`,`Basic Electrical Engineering`,`id_r`) VALUES (%s,%s,%s,%s,%s,%s)",(Subj1,Subj2,Subj3,Subj4,Subj5,rl))
            conn.commit()
            conn.close()
        return render_template('pg.html')


if __name__ == '__main__':
    app.run(debug=True)
