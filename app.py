from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# A dictionary to store user credentials (for demonstration purposes)
users = {
    'admin': 'admin',
    'user1': 'password1',
    'user2': 'password2'
}

# A dictionary to store user calculation history (for demonstration purposes)
calculation_history = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect('/calculator')
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')


# Route for the calculator page
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('/')
    
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operator = request.form['operator']
        result = perform_calculation(num1, num2, operator)
        
        save_history = request.form.get('save_history')
        if save_history:
            save_calculation(session['username'], num1, num2, operator, result)
        
        return render_template('calculator.html', result=result)

    return render_template('calculator.html')

# Perform calculation based on the operator
def perform_calculation(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2

# Save calculation history
def save_calculation(username, num1, num2, operator, result):
    if username not in calculation_history:
        calculation_history[username] = []
    
    calculation = {
        'num1': num1,
        'num2': num2,
        'operator': operator,
        'result': result
    }
    calculation_history[username].append(calculation)

# Route for the admin dashboard
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin/login')
    
    return render_template('admin_dashboard.html', history=calculation_history)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error='Invalid username or password.')

    return render_template('admin_login.html')


# Route to disable a user
@app.route('/admin/disable/<username>')
def disable_user(username):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin/login')
    
    if username in users:
        del users[username]
        if username in calculation_history:
            del calculation_history[username]
    
    return redirect('/admin')

# Route for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
