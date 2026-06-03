from flask import Flask, render_template, request,url_for,redirect

app = Flask(__name__)
@app.route('/')
def home():
    return redirect('/login')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        return f"""
        <h2>Registration Successful!</h2>
        <p>Name: {name}</p>
        <p>Email: {email}</p>
        """

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