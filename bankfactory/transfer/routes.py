from flask import render_template,url_for,flash,redirect,request,Blueprint
from bankfactory.transfer.forms import AddPayee,BeginPayment
from bankfactory import bcrypt
from functools import wraps
from Utils.ConfigReader import getInstance
from Utils.DBConnectivity import DBConnectivity
from Utils.GmailFactory import send_email
from bankfactory import session
from numpy import double


transfer = Blueprint('transfer',__name__)



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



@transfer.route('/transferfunds',methods=['GET','POST'])
@is_logged_in
def transferfunds():
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    query = "select * from PAYEE where ACCOUNTNO='"+session['AccountNo']+"'"
    payee_list = DBConnectivity.getQueryResult(con, query).fetchall()
    
    if request.method == "POST":
        if request.form['buttonaction'] == "Remove Payee":
            if len(payee_list) == 0:
                flash("No Records Found for Remove payee","info")
                return redirect(url_for('transfer.transferfunds'))
            else:
                payee_account_no_to_be_deleted = request.form['payeeaccountno']
                query = "Delete from PAYEE where PAYEEACCOUNTNO='"+payee_account_no_to_be_deleted+"' and ACCOUNTNO='"+session['AccountNo']+"'"
                DBConnectivity.updateDatabase(con, query)
                flash("Payee has been successfully Deleted !","success")
                return redirect(url_for('transfer.transferfunds'))
        else:
            if len(payee_list) == 0:
                flash("Add Payee for fund transfer","info")
                return redirect(url_for('transfer.addpayee'))
            else:
                try:
                    session['PayeeAccountNo'] = request.form['payeeaccountno']
                    return redirect(url_for('transfer.beginpayment'))
                except:
                    flash("Select at least one payee for transfer fund","info")
                    return redirect(url_for('transfer.transferfunds'))
        
    return render_template("transferfunds.html",payee_list=payee_list)

@transfer.route('/beginpayment',methods=['GET','POST'])
@is_logged_in
def beginpayment():
    form = BeginPayment()
    
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    query = "select * from PAYEE where ACCOUNTNO='"+session['AccountNo']+"' and PAYEEACCOUNTNO='"+session['PayeeAccountNo']+"'"
    payee = DBConnectivity.getQueryResult(con, query).fetchone()
    if form.validate_on_submit():
        query = "select * from bankdetails where ACCOUNTNO='"+session['AccountNo']+"'"
        account_details = DBConnectivity.getQueryResult(con, query).fetchone()
        from_balance = account_details[3]
        
        query = "select * from bankdetails where ACCOUNTNO='"+session['PayeeAccountNo']+"'"
        account_details = DBConnectivity.getQueryResult(con, query).fetchone()
        to_balance = account_details[3]
        
        if from_balance >= double(form.amount.data):
            query = "select * from payee where ACCOUNTNO='"+session['AccountNo']+"' and PAYEEACCOUNTNO='"+session['PayeeAccountNo']+"'"
            payee = DBConnectivity.getQueryResult(con,query).fetchone()
            
            query = "select * from customer where ACCOUNTNO='"+session['AccountNo']+"'"
            customer = DBConnectivity.getQueryResult(con, query).fetchone()
            
            query = "update bankdetails set BALANCE="+str((from_balance - double(form.amount.data)))+" where ACCOUNTNO='"+session['AccountNo']+"'"
            DBConnectivity.updateDatabase(con, query)
            
            query = "update bankdetails set BALANCE="+str((double(form.amount.data)+to_balance))+" where ACCOUNTNO='"+session['PayeeAccountNo']+"'"
            DBConnectivity.updateDatabase(con, query)
            
            Transaction_Details1 = "To : "+form.payement_type.data+"/"+session['PayeeAccountNo']+"/"+payee[2]
            Transaction_Details2 = "From : "+form.payement_type.data+"/"+session['AccountNo']+"/"+customer[3]
            
            from_amount = str((from_balance-double(form.amount.data)))
            to_amount = str((to_balance+double(form.amount.data)))
            
            query1 = "INSERT INTO TRANSACTION(ACCOUNTNO,TRANSACTIONDETAILS,AMOUNT,TRANSACTIONTYPE,BALANCE) VALUES('"+session['AccountNo']+"','"+Transaction_Details1+"',"+str(form.amount.data)+",'D',"+from_amount+")"
            query2 = "INSERT INTO TRANSACTION(ACCOUNTNO,TRANSACTIONDETAILS,AMOUNT,TRANSACTIONTYPE,BALANCE) VALUES('"+session['PayeeAccountNo']+"','"+Transaction_Details2+"',"+str(form.amount.data)+",'C',"+to_amount+")"
            
            DBConnectivity.updateDatabase(con,query1)
            DBConnectivity.updateDatabase(con,query2)
            flash("Your payment has been successfully transfered", "success")
            return redirect(url_for("transfer.transferfunds"))
        else:
            flash("Insufficient Balance","danger")
            return redirect(url_for("transfer.beginpayment"))
    return render_template("beginpayment.html",form=form,payee=payee)

@transfer.route('/addpayee',methods=['GET','POST'])
@is_logged_in
def addpayee():
    form=AddPayee()
    
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    
    if form.validate_on_submit():
        query = "select * from customer c join bankdetails b on c.ACCOUNTNO= b.ACCOUNTNO where c.ACCOUNTNO='"+form.payee_account_number.data+"'"
        payee = DBConnectivity.getQueryResult(con, query).fetchone()
        if payee != None:
            branch_name = form.payee_branch_name.data[0].upper()+form.payee_branch_name.data[1:].lower()
            print(payee[6],form.payee_email.data,payee[11],branch_name,payee[12],form.payee_ifsc.data)
            if payee[6] == form.payee_email.data and payee[11] == branch_name and payee[12] == form.payee_ifsc.data:
                query = "select * from PAYEE where ACCOUNTNO='"+session['AccountNo']+"' and PAYEEACCOUNTNO='"+form.payee_account_number.data+"'"
                customer = DBConnectivity.getQueryResult(con, query).fetchone()
                if customer == None:
                    query = "insert into PAYEE(ACCOUNTNO,PAYEEACCOUNTNO,PAYEENAME,EMAILID,BANKNAME,BRANCHNAME,IFSC) values('" \
                            +session['AccountNo']+"','"+form.payee_account_number.data+"','"+form.payee_name.data+"','"+form.payee_email.data+"','" \
                            +form.payee_bank_name.data+"','"+branch_name+"','"+form.payee_ifsc.data+"')"
                    DBConnectivity.updateDatabase(con, query)
                    flash(form.payee_name.data+" has been successfully added to your account as payee", "success")
                    return redirect(url_for('transfer.transferfunds'))
                else:
                    flash("Payee has already added to your account","info")
                    return redirect(url_for("transfer.transferfunds"))
            else:
                flash("Invalid Details","info")
                return redirect(url_for("transfer.addpayee"))
        else:
            flash("Payee has not registered with Bank Application","info")
            return redirect(url_for("transfer.transferfunds"))
    return render_template("addpayee.html",form=form)
