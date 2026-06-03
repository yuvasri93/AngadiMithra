from flask import Flask, render_template, request,url_for,redirect
import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'  
load_dotenv(dotenv_path=env_path)          
app = Flask(__name__)
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "angadimithra")
)
@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        sql="""INSERT INTO users(name,email,password)VALUES(%s,%s,%s)"""
        values=(name,email,password)
        cursor=db.cursor()
        cursor.execute(sql,values)
        db.commit()
        cursor.close()
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        return "Login Successful"

    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)