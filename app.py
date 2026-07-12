from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('dashboard/landing.html')

@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/home')
def home():
    return render_template('dashboard/home.html')

@app.route('/interns')
def interns():
    return render_template('dashboard/internship.html')

@app.route('/sessions')
def sessions():
    return render_template('dashboard/sessions.html')

@app.route('/rewards')
def rewards():
    return render_template('dashboard/rewards.html')

@app.route('/skills')
def skills():
    return render_template('dashboard/skills.html')

@app.route('/realm')
def realm():
    return render_template('realm.html')

@app.route('/certify')
def certify():
    return render_template('dashboard/certificate.html')

@app.route('/community')
def community():
    return render_template('dashboard/community.html')

@app.route('/leaderboard')
def lead():
    return render_template('dashboard/leaderboard.html')

@app.route('/setting')
def setting():
    return render_template('auth/settings.html')

if __name__ == '__main__':
    app.run(debug=True)
    