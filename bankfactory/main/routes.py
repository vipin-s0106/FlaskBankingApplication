from flask import render_template,url_for,flash,redirect,request,Blueprint
from functools import wraps
from bankfactory import session

main = Blueprint('main',__name__)



#check User logged off or not
def is_logged_off(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized, Please Logout", "danger")
            return redirect(url_for("customer.dashboard"))      
    return wrap



@main.route("/")
@is_logged_off
def home():
    return render_template("home.html")
