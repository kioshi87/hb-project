"""Server for movie ratings app."""

from flask import Flask

app = Flask(__name__)


# Replace this with routes and view functions!
@app.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']

    user = get_user_by_email(email)
    if user:
        return 'A user already exists with that email.'
    else:
        create_user(email, password, username)

        return redirect('/login-form')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
