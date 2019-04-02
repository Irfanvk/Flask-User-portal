from flask import Flask, render_template, request, session, redirect, escape, url_for
from models import db, User
from forms import SignupForm, LoginForm

app = Flask(__name__)
# 'postgresql://postgres:postgres@localhost:5432/flask_1'
# 'DB_service://username:password@addres:port/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flask_1'
db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
    # if email in session:
    #     return 'Logged in as %s' % escape(session['email'])
    # return 'You are Logged in'
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data,
                           form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html')
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                print(session)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
