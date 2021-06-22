from flask import Flask,render_template,request,redirect,session,flash
from flask_session import Session
import pyrebase
import os

app=Flask(__name__)

app.secret_key = os.urandom(24)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

firebaseConfig={
    "apiKey": "apiKey",
    "authDomain": "projectId.firebaseapp.com",
    "databaseURL": "https://databaseName.firebaseio.com",
    "storageBucket": "projectId.appspot.com",
    "serviceAccount": "path/to/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()

db=firebase.database()


@app.route("/")
def home():
    if 'user' in session :
        return redirect("/dashboard")
    return render_template("index.html")


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if 'user' in session :
        username = session['user'].replace('.','_')
        if request.method=="POST":
            title = request.form['title']
            desc = request.form['desc']
            date = request.form['date']
            time = request.form['time']
            db.child(username).push({"title":title,"description":desc,"deadline_date":date,"deadline_time":time})
        all_todos = db.child(username).get()
        return render_template('dashboard.html',all_todos=all_todos)
    return redirect("/")


@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == "POST" :
        email=request.form['email']
        pw=request.form['pw']
        pwr=request.form['pwr']
        if pw==pwr :
            if len(pw)>=8 :
                try:
                    user=auth.create_user_with_email_and_password(email,pw)
                    auth.send_email_verification(user['idToken'])
                    flash("Account created successfully. You can now Login using your account.","success")
                    return redirect("/login")
                except:
                    flash("Email already exists","danger")
            else:
                flash("Weak password. Length of password should be atleast 8 characters.","danger")
        else:
            flash("Passwords didn't match.","danger")
    return render_template("signup.html")


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST" :
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email=email,password=password)
            user = auth.refresh(user['refreshToken'])
            session['user'] = email
            return redirect("/dashboard")
        except:
            flash("Invalid email or password","danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    if 'user' in session :
        message = session['user'] + " logged out successfully."
        session.pop('user')
        flash(message,"success")
        return redirect("/")
    return redirect("/")


@app.route("/update/<string:id>",methods=['GET','POST'])
def update(id):
    if 'user' in session :
        username = session['user'].replace('.','_')
        if request.method=='POST' :
            title = request.form['title']
            desc = request.form['desc']
            date = request.form['date']
            time = request.form['time']
            db.child(username).child(id).update({"title":title,"description":desc,"deadline_date":date,"deadline_time":time})
            return redirect("/dashboard")
        todo = db.child(username).child(id).get()
        return render_template('update.html',todo=todo)
    return redirect("/")


@app.route("/delete/<string:id>")
def delete(id):
    if 'user' in session :
        username = session['user'].replace('.','_')
        db.child(username).child(id).remove()
        return redirect("/dashboard")
    return redirect("/")


@app.route("/forgot-password",methods=['GET','POST'])
def reset_password():
    if 'user' in session :
        if request.method == "POST" :
            email=request.form['email']
            auth.send_password_reset_email(email)
            flash("Password reset email sent successfully. Follow instructions given in the email to reset your password.","success")
    return redirect("/")


@app.route("/delete-account",methods=['GET','POST'])
def delete_account() :
    if 'user' in session :
        if request.method == "POST" :
            password=request.form['password']
            try:
                user=auth.sign_in_with_email_and_password(email=session['user'],password=password)
                auth.delete_user_account(user['idToken'])
                username = session['user'].replace('.','_')
                db.child(username).remove()
                session.pop('user')
                flash("Account deleted successfully.","success")
                return redirect("/")
            except:
                flash("Invalid credentials","danger")
                return redirect("/dashboard")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
