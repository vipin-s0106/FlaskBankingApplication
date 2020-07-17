from flask import render_template,url_for,flash,redirect,request,Blueprint
from bankfactory import bcrypt
from functools import wraps
from Utils.ConfigReader import getInstance
from Utils.DBConnectivity import DBConnectivity
from bankfactory.customer.utils import *
from Utils.GmailFactory import send_email
import random
from bankfactory import session
from Utils import GmailFactory

loans = Blueprint('loans',__name__)



#check User logged in or not
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized, Please Login", "danger")
            return redirect(url_for("customer.login"))      
    return wrap



@loans.route('/loan')
@is_logged_in
def loan():
   return render_template('loan.html')