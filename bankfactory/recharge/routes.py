from flask import render_template,url_for,flash,redirect,request,Blueprint
from bankfactory.recharge.forms import MobileRecharge,DTHRecharge,ElecRecharge
from bankfactory import bcrypt
from functools import wraps
from Utils.ConfigReader import getInstance
from Utils.DBConnectivity import DBConnectivity
from Utils.GmailFactory import send_email
from bankfactory import session
from numpy import double


recharge = Blueprint('recharge',__name__)



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

@recharge.route('/rechargehome')
@is_logged_in
def rechargehome():
    return render_template("rechargehome.html")





@recharge.route('/rechargemobile',methods=['GET','POST'])
@is_logged_in
def rechargemobile():
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    
    form = MobileRecharge()
    if form.validate_on_submit():
        if form.mobileno.data < 9999999999 and form.mobileno.data > 9999999:
            query = "select * from bankdetails where ACCOUNTNO='"+session['AccountNo']+"'"
            customer = DBConnectivity.getQueryResult(con, query).fetchone()
            balance = customer[3]
            recharge_balance = int(form.mobileplan.data.split(" ")[0])
            recharge_balance = double(recharge_balance)
            if(balance >= recharge_balance):
                account_balance = balance - recharge_balance
                Transaction_Details = "To : MobileRecahrge/"+str(form.mobileno.data)+"/"+form.provider.data+" Service Provider"
                query1 = "INSERT INTO TRANSACTION(ACCOUNTNO,TRANSACTIONDETAILS,AMOUNT,TRANSACTIONTYPE,BALANCE) VALUES('"+session['AccountNo']+"','"+Transaction_Details+"',"+str(recharge_balance)+",'D',"+str(account_balance)+")"
                query2 = "update bankdetails set BALANCE="+str(account_balance)+" where ACCOUNTNO='"+session['AccountNo']+"'"
                
                DBConnectivity.updateDatabase(con, query1)
                DBConnectivity.updateDatabase(con, query2)
                flash("Your mobile has been successfully Recharged","success")
                return redirect(url_for('recharge.rechargemobile'))
            else:
                flash("Insufficient Balance","danger")
                return redirect(url_for('recharge.rechargemobile'))
        else:
            flash("Wrong Mobile No","danger")
            return redirect(url_for('recharge.rechargemobile'))
    return render_template("rechargemobile.html",form=form)


@recharge.route('/rechargedth',methods=['GET','POST'])
@is_logged_in
def rechargedth():
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    
    
    form = DTHRecharge()
    if form.validate_on_submit():
        query = "select * from bankdetails where ACCOUNTNO='"+session['AccountNo']+"'"
        customer = DBConnectivity.getQueryResult(con, query).fetchone()
        balance = customer[3]
        recharge_balance = int(form.dthplan.data.split(" ")[0])
        recharge_balance = double(recharge_balance)
        if(balance >= recharge_balance):
            account_balance = balance - recharge_balance
            Transaction_Details = "To : DTH Recahrge/"+form.consumerno.data+"/"+form.dthprovider.data+" Service Provider"
            query1 = "INSERT INTO TRANSACTION(ACCOUNTNO,TRANSACTIONDETAILS,AMOUNT,TRANSACTIONTYPE,BALANCE) VALUES('"+session['AccountNo']+"','"+Transaction_Details+"',"+str(recharge_balance)+",'D',"+str(account_balance)+")"
            query2 = "update bankdetails set BALANCE="+str(account_balance)+" where ACCOUNTNO='"+session['AccountNo']+"'"
            
            DBConnectivity.updateDatabase(con, query1)
            DBConnectivity.updateDatabase(con, query2)
            flash("Your DTH Bill has been successfully submitted","success")
            return redirect(url_for('recharge.rechargedth'))
        else:
            flash("Insufficient Balance","danger")
            return redirect(url_for('recharge.rechargedth'))
    return render_template("rechargedth.html",form=form)


@recharge.route('/rechargeelec',methods=['GET','POST'])
@is_logged_in
def rechargeelec():
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    
    form = ElecRecharge()
    if form.validate_on_submit():
        query = "select * from bankdetails where ACCOUNTNO='"+session['AccountNo']+"'"
        customer = DBConnectivity.getQueryResult(con, query).fetchone()
        balance = customer[3]
        recharge_balance = double(form.amount.data)
        if(balance >= recharge_balance):
            account_balance = balance - recharge_balance
            Transaction_Details = "To : Electricity Bill/consumer:"+form.consumerno.data+"/"+form.provider.data+" pvt LTD"
            query1 = "INSERT INTO TRANSACTION(ACCOUNTNO,TRANSACTIONDETAILS,AMOUNT,TRANSACTIONTYPE,BALANCE) VALUES('"+session['AccountNo']+"','"+Transaction_Details+"',"+str(recharge_balance)+",'D',"+str(account_balance)+")"
            query2 = "update bankdetails set BALANCE="+str(account_balance)+" where ACCOUNTNO='"+session['AccountNo']+"'"
            
            DBConnectivity.updateDatabase(con, query1)
            DBConnectivity.updateDatabase(con, query2)
            flash("Your Electricity Bill has been successfully submitted","success")
            return redirect(url_for('recharge.rechargedth'))
        else:
            flash("Insufficient Balance","danger")
            return redirect(url_for('recharge.rechargedth'))
    return render_template("rechargeelec.html",form=form)
    