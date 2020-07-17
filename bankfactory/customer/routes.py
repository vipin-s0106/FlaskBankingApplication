from flask import render_template,url_for,flash,redirect,request,Blueprint
from bankfactory.customer.forms import RegistrationForm,LoginForm,SetPassword,ForgotPassword
from bankfactory import bcrypt,app
from functools import wraps
from Utils.ConfigReader import getInstance
from Utils.DBConnectivity import DBConnectivity
from Utils.GmailFactory import send_email
import random,os
from bankfactory import session
from werkzeug.utils import secure_filename

customer = Blueprint('customer',__name__)



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

#check User logged off or not
def is_logged_off(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized, Please Logout", "danger")
            return redirect(url_for("main.home"))      
    return wrap



@customer.route('/login',methods=['GET','POST'])
@is_logged_off
def login():
    form = LoginForm()
    if form.validate_on_submit():
        reader = getInstance()
        con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
        
        query = "select * from customer where CUSTOMERID='"+form.customerid.data+"'"
        cursor = DBConnectivity.getQueryResult(con, query)
        customer = cursor.fetchone()
        if customer != None:
            hashed_pwd = customer[2]
            if(bcrypt.check_password_hash(hashed_pwd,form.password.data)): 
                if customer[8] == 'Y':
                    session['logged_in'] = True
                    session['AccountNo'] = customer[1]
                    return redirect(url_for("customer.setPassword"))
                else:
                    session['logged_in'] = True
                    session['AccountNo'] = customer[1]
                    return redirect(url_for("customer.dashboard"))
            else:
                flash("Invalid Password !","danger")
                return redirect(url_for("customer.login"))
        else:
            flash("You have not Registered ! Please Register","danger")
            return redirect(url_for("customer.register"))
    return render_template("login.html",form=form)


@customer.route('/setPassword',methods=['GET','POST'])
@is_logged_in
def setPassword():
    form = SetPassword()
    if form.validate_on_submit():
        reader = getInstance()
        con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
        
        query = "select * from customer where ACCOUNTNO='"+session['AccountNo']+"'"
        cursor = DBConnectivity.getQueryResult(con, query)
        customer = cursor.fetchone()
        if bcrypt.check_password_hash(customer[2],form.OTP.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            query = "update customer set PASSWORD='"+hashed_password+"' WHERE ACCOUNTNO='"+session['AccountNo']+"'"
            DBConnectivity.updateDatabase(con, query)
            query = "update customer set LOGINSTATUS='N' WHERE ACCOUNTNO='"+session['AccountNo']+"'"
            DBConnectivity.updateDatabase(con, query)
            return redirect(url_for("customer.dashboard"))
        else:
            flash("You have entered wrong OTP","danger")
            return redirect(url_for("customer.setPassword"))
    return render_template("setPassword.html",form=form)


@customer.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")


@customer.route('/register',methods=['GET','POST'])
@is_logged_off
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        reader = getInstance()
        con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
        
        temp_pwd = chr(random.randrange(65,97))+str(random.randrange(0,10))+chr(random.randrange(65,97))+str(random.randrange(0,10)) \
                   +chr(random.randrange(65,97))+str(random.randrange(0,10))
        hashed_password = bcrypt.generate_password_hash(temp_pwd).decode('utf-8')
        
        query = "select * from customer where ACCOUNTNO='"+form.account_number.data+"'"
        cursor = DBConnectivity.getQueryResult(con, query)
        cursor = cursor.fetchone()
        if(cursor == None):
            query = "select * from customer where EMAILID='"+form.email.data+"'"
            cursor = DBConnectivity.getQueryResult(con, query)
            cursor = cursor.fetchone()
            if(cursor == None):
                #updating Customer table
                name = form.account_holder_name.data.split(" ")
                customer_name = ""
                for i in range(0,len(name)):
                    if i == len(name)-1:
                        customer_name += name[i][0].upper()+name[i][1:].lower()
                    else:
                        customer_name += name[i][0].upper()+name[i][1:].lower()+" "
                query = "Insert into customer(ACCOUNTNO,PASSWORD,CUSTOMERNAME,COUNTRY,MOBILENO,EMAILID,DATEOFBIRTH,LOGINSTATUS,PROFILEPICTURE) values('" \
                +form.account_number.data+"','"+hashed_password+"','"+customer_name+"','"+form.country.data+"',"+form.mobile_no.data+",'" \
                +form.email.data+"','"+str(form.dob.data)+"','Y','profile.png')"
                DBConnectivity.updateDatabase(con, query)
                
                #updating BankDetails table
                branch_name = form.branch_name.data[0].upper()+form.branch_name.data[1:].lower()
                query = "Insert into bankdetails(ACCOUNTNO,BRANCHNAME,IFSC,BALANCE) values('"+form.account_number.data+"','" \
                        +branch_name+"','"+form.ifsc.data+"',1000)"
                DBConnectivity.updateDatabase(con, query)
                
                query = "select * from customer where EMAILID='"+form.email.data+"'"
                cursor = DBConnectivity.getQueryResult(con, query)
                customer = cursor.fetchone()
                msg = "Hello "+form.account_holder_name.data+"!!\n\n\n" \
                      +"Your CustomerID is "+str(customer[0])+".\n"+str(temp_pwd)+" is your temporary password for login to the Axis Bank application"
                      
                send_email("Axis Bank Application Alerts",msg, form.email.data)
                
                flash("You have successfully Registered!","success")
                return redirect(url_for("customer.login"))
            else:
                flash("Email-ID has already Registered", "danger")
                return redirect(url_for("customer.register"))
        else:
            flash("Customer has already Registered", "danger")
            return redirect(url_for("customer.register"))
    return render_template("register.html",form=form,captcha="123456")


@customer.route("/dashboard")
@is_logged_in
def dashboard():
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    query = "select * from BANKDETAILS where ACCOUNTNO='"+session['AccountNo']+"'" 
    cursor = DBConnectivity.getQueryResult(con, query)
    cursor = cursor.fetchone() 
    return render_template("dashboard.html",balance=cursor[3])


@customer.route('/forgot_password',methods=['GET','POST'])
@is_logged_off
def forgot_password():
    form = ForgotPassword()
    
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
      
    if form.validate_on_submit():
        temp_pwd = chr(random.randrange(65,97))+str(random.randrange(0,10))+chr(random.randrange(65,97))+str(random.randrange(0,10)) \
                       +chr(random.randrange(65,97))+str(random.randrange(0,10))
        hashed_password = bcrypt.generate_password_hash(temp_pwd).decode('utf-8')
        
        query = "select * from CUSTOMER where ACCOUNTNO='"+form.account_number.data+"' and EMAILID = '"+form.email.data+"'"
        customer = DBConnectivity.getQueryResult(con, query).fetchone()
        if customer != None:
            query = "update customer set PASSWORD='"+hashed_password+"',LOGINSTATUS='Y' where ACCOUNTNO='"+form.account_number.data+"' and EMAILID = '"+form.email.data+"'"
            DBConnectivity.updateDatabase(con, query)
            msg = temp_pwd+"  is your one time password using that you can login to application" \

            send_email("no reply : Password Reset", msg, form.email.data)
            flash("Your new OTP has been sent to your registered Email ID !","info")
            return redirect(url_for('customer.login'))
        else:
            flash("You haven't register with us !","danger")
            return redirect(url_for('customer.register'))
    return render_template("forgot_password.html",form=form)


@customer.route('/account',methods=['GET','POST'])
@is_logged_in
def account():
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
    
    query = "select * from customer where ACCOUNTNO='"+session['AccountNo']+"'"
    customer = DBConnectivity.getQueryResult(con, query).fetchone()
    
    image_file = url_for('static',filename='profile/'+customer[9])
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part','info')
            return redirect(url_for('customer.account'))
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            query = "update customer set PROFILEPICTURE='"+filename+"' where ACCOUNTNO='"+session['AccountNo']+"'"
            DBConnectivity.updateDatabase(con, query)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Your profile picture has been successfully updated !',"success")
            return redirect(url_for('customer.account'))
    return render_template('account.html',customer = customer,image_file=image_file)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

