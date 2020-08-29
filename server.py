from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_bcrypt import Bcrypt 
from datetime import datetime
from mysqlconnection import connectToMySQL

# the "re" module will let us perform some regular expression operations
import re
import pymysql
#makes data sent in the form of python dictionaries
import pymysql.cursors 

#connect DB
mysql = connectToMySQL('registrationsdb')

# used for email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ThisIsSecret!"

# Models - DB/ Shape
# View - view of page
# Controller - Logic


# Create - METHOD POST - SQL terminialogy -INSERT INTO
# Read - METHOD GET - SQL terminialogy - SELECT
# Update - METHOD POST/ PUT - SQL terminialogy - UPDATE
# Delete - METHOD POST/ DELETE- SQL terminialogy - DELETE

# snake casing - first_name, last_name
# camel casing - firstName, lastName
# pascal casing - FirstName, LastName


@app.route('/')
def index():
    return render_template('index.html')
# ==============================================

@app.route('/register', methods=['GET', 'POST'])
def process():
    # if method is post
    if request.method == 'POST': 
        # name validation
        # --------------------------------------
        if len(request.form['first_name']) < 2:
            flash("first name must be at least 2 characters", 'f-name')
        if len(request.form['last_name']) < 2:
            flash("last name must be at least 2 characters", 'l-name')

        # new-email validation
        # --------------------------------------
        if not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid Email Address!", 'email')


        # checking if email exist
        mysql = connectToMySQL("registrationsdb")
        searchQuery = "SELECT * FROM users WHERE email = %(email)s;"
        param = {
            "email": request.form["email"]
        }
        searchResults = mysql.query_db(searchQuery, param)
        if searchResults:
            flash('User already exist in database', 'existing')
        # print(searchQuery)
        # data = { "email" : request.form['new-email']}
        # matchingEmail = mysql.query_db(searchQuery, data)

        #     if matchingEmail already exists")
        #         return redirect("/")
        # Email:
        #         flash("
        # # new-password validation
        # # --------------------------------------
        if len(request.form['password_hash']) < 8:
            flash("password must be at least 8 characters", 'new-password')
        
        # # confirm-password validation
        # # --------------------------------------
        if request.form['password_hash'] != request.form['confirm_password']:
            flash("passwords don't match", 'confirm-password')

        else: 
            mysql = connectToMySQL("registrationsdb")
            pw_hash = bcrypt.generate_password_hash(request.form['password_hash'])
            data = {
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "email": request.form['email'],
                "password_hash": pw_hash
            }
            query = "INSERT INTO users (first_name, last_name, email, password_hash, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s,  NOW(), NOW());"
            mysql.query_db(query, data)
            # return render_template('index.html')
            return redirect("/success")
        
    else:
        return render_template('index.html')
        
    # # login-email validation
    # # --------------------------------------
    # if len(request.form['login-email']) < 1: 
    #     flash("Email cannot be blank!", 'login-email')
    # if not EMAIL_REGEX.match(request.form['login-email']):
    #     flash("Invalid Email Address!", 'login-email')
        # YAY ADD EMAIL TO DATABASE 
        # ==========================
        # else:
        #     # getting current datetime
        #     createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     print("CREATED AT", createdAt)

        #     mysql = connectToMySQL('emailsdb')
        #     query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s," + "'" + createdAt +"'," + "'" + createdAt +"');"     
        #     data = { 'email': userEmail }
        #     mysql.query_db(query, data)

        #     # return redirect("/success")    # change route later
        #     return render_template("success.html", email = userEmail)
        #     #  currentUser = userEmail)

# ==============================================


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST': 
        # Validating email format
        if not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid Email Address!", 'login-email')

        # validate password length
        if len(request.form['login_password']) < 8:
            flash("password must be at least 8 characters", 'login-password')

        else:
            mysql = connectToMySQL("registrationsdb")
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = { "email": request.form['email'] }
            result = mysql.query_db(query, data)

            if result:
                print('working1')
                if bcrypt.check_password_hash(result[0]['password_hash'], request.form['login_password']):
                    print('working2')
                    session['richard_id'] = result[0]['id']
                    return render_template('index.html')

            print('not-working')
            flash('You could not logged in')
            return redirect('/321')

    else:
        render_template('index.html')

# ==============================================
# ==============================================

@app.route('/success')
# # @app.route('/success', methods=['GET'])
def success():
    print(session['richard_id'])
    return redirect('/')
#     mysql = connectToMySQL('emailsdb')
#     lastFiveEmails = mysql.query_db("SELECT * FROM emails ORDER BY id DESC limit 5")
#     print("DATA:", lastFiveEmails)

#     return render_template('success.html', email = lastFiveEmails)

# ==============================================
# starts the server
if __name__ == "__main__":
    app.run(debug=True)

# ==============================================

