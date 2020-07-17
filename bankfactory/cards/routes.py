from flask import render_template,url_for,flash,redirect,request,Blueprint
from bankfactory.cards.forms import AddCards
from bankfactory import bcrypt
from functools import wraps
from Utils.ConfigReader import getInstance
from Utils.DBConnectivity import DBConnectivity
from bankfactory import session

cards = Blueprint('cards',__name__)



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




@cards.route('/carddetails',methods=['GET','POST'])
@is_logged_in
def carddetails():
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    query = "select * from CARDDETAILS where ACCOUNTNO='"+session['AccountNo']+"' and CARDTYPE='C'"
    cursor = DBConnectivity.getQueryResult(con, query)
    credit_card = cursor.fetchall()  
    
    query = "select * from CARDDETAILS where ACCOUNTNO='"+session['AccountNo']+"' and CARDTYPE='D'"
    cursor = DBConnectivity.getQueryResult(con, query)
    debit_card = cursor.fetchall()
    
    if(request.method == "POST"):
        if request.form['buttonaction'] == "Activate":
            query = "select * from CARDDETAILS where CARDNO='"+request.form['option']+"'"
            card_type = DBConnectivity.getQueryResult(con, query).fetchone()[3]
            
            query = "select count(*) from CARDDETAILS where ACCOUNTNO='"+session['AccountNo']+"' and CARDTYPE='"+card_type+"' and status='Active'"
            count_value = DBConnectivity.getQueryResult(con, query).fetchone()[0]
            
            if count_value == 0:
                query = "update CARDDETAILS set status='Active' where CARDNO='"+request.form['option']+"'"
                DBConnectivity.updateDatabase(con, query)
                flash("Your card has been successfully Activated !","success")
            else:
                flash("You can't have more than 1 card Activated !","danger")
            
        elif request.form['buttonaction'] == "Deactivate":
            query = "update CARDDETAILS set status='Inactive' where CARDNO='"+request.form['option']+"'"
            DBConnectivity.updateDatabase(con, query)
            flash("Your card has been successfully De-activated !","success")
        return redirect(url_for('cards.carddetails'))
    return render_template("carddetails.html",credit_card=credit_card,debit_card=debit_card)

@cards.route('/addcards',methods=['GET','POST'])
@is_logged_in
def addcards():
    form = AddCards()
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    query = "select * from customer where ACCOUNTNO='"+session['AccountNo']+"'"
    cursor = DBConnectivity.getQueryResult(con, query)
    customer = cursor.fetchone()
    if form.validate_on_submit():
        if form.card_type.data == "Credit Card":
            query = "select count(*) from CARDDETAILS where ACCOUNTNO='"+session['AccountNo']+"' and CARDTYPE='C' and status='Active'"
            count_value = DBConnectivity.getQueryResult(con, query).fetchone()[0]
            if count_value == 0:
                query = "insert into carddetails(ACCOUNTNO,CARDNO,CARDHOLDERNAME,CARDTYPE,CVV,PIN,STATUS) values('"+session['AccountNo']+ \
                        "','"+form.card_no.data+"','"+form.card_holder_name.data+"','C','"+form.cvv.data+"','"+form.pin.data+"','Active')"
                DBConnectivity.updateDatabase(con, query)
                flash("Credit Card has been successfully added !","success")
            else:
                flash("You can't add more that 1 activated Credit card !","danger")
            return redirect(url_for("cards.carddetails"))
        elif form.card_type.data == "Debit Card":
            query = "select count(*) from CARDDETAILS where ACCOUNTNO='"+session['AccountNo']+"' and CARDTYPE='D' and status='Active'"
            count_value = DBConnectivity.getQueryResult(con, query).fetchone()[0]
            if count_value == 0:
                query = "insert into carddetails(ACCOUNTNO,CARDNO,CARDHOLDERNAME,CARDTYPE,CVV,PIN,STATUS) values('"+session['AccountNo']+ \
                        "','"+form.card_no.data+"','"+form.card_holder_name.data+"','D','"+form.cvv.data+"','"+form.pin.data+"','Active')"
                DBConnectivity.updateDatabase(con, query)
                flash("Debit Card has been successfully added !","success")
            else:
                flash("You can't add more that 1 activated Debit card !","danger")
            return redirect(url_for("cards.carddetails"))
        else:
            pass
    form.card_holder_name.data = customer[3] 
    return render_template("addcards.html",form=form)



