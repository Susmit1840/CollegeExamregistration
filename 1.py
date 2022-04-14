from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL




app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testingdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/personal',methods=['GET', 'POST'])
def personal(request):
    conn = mysql.connect()
    cursor = conn.cursor(mysql.cursors.DictCursor)
    
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
            cursor.execute("INSERT INTO `personal_details`(`id`, `Name`, `DOB`, `Gender`, `contact`, `address`, `email`, `department`, `year`, `semester`, `user_id`) VALUES (fullname,dob,'gender','phoneno','address','emailid','department','year','semester','user_id'")  
            conn.commit()
    
            return render_template('personal_details.html',username=session['username'])