from flask import render_template,url_for,flash,redirect,Blueprint,request
from bankfactory.statement.forms import GetStatement
from bankfactory import bcrypt
from functools import wraps
from Utils.ConfigReader import getInstance
from Utils.DBConnectivity import DBConnectivity
from Utils.GmailFactory import send_email
import random,time
from bankfactory import session

statement = Blueprint('statement',__name__)



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


@statement.route("/getStatement",methods=['GET','POST'])
@is_logged_in
def getStatement():
    form=GetStatement()
    if request.method == "POST":
        from_date = str(form.from_date.data)
        to_date = str(form.to_date.data)
        period = str(form.period.data)
        if from_date != 'None' and to_date != 'None':
            date = from_date+";"+to_date
        else:
            date = period
        return redirect(url_for("statement.printStatement",date=date))
    return render_template("getStatement.html",form=form)


@statement.route("/printStatement/<string:date>")
@is_logged_in
def printStatement(date):
    reader = getInstance()
    con = DBConnectivity.getConnection(reader.get("Credential", "hostname"),reader.get("Credential", "username"), reader.get("Credential", "password"), reader.get("Credential", "database"))
        
    date = date.split(";")
    if(len(date) > 1):
        temp_date = date[1]
        date[1] = date[1][0:9]+str(int(date[1][9:11]) + 1)
        query = "select * from transaction where transactiondate between '"+date[0]+"' and '"+date[1]+"' and accountno='"+session['AccountNo']+"' order by transactiondate desc"
        cursor = DBConnectivity.getQueryResult(con, query)
        transaction = cursor.fetchall()
        if len(transaction) >= 1:
            return render_template("printStatement.html",transaction=transaction)
        else:
            flash("No Record found between "+date[0]+" and "+temp_date,"danger")
            return redirect(url_for('statement.getStatement'))
    else:
        if(date[0]=="Last One Week"):
            date1 = time.strftime("%Y-%m-%d")
            if(int(date1[8:10]) < 7):
                month = int(date1[5:7])-1
                if month < 1:
                    year = int(date1[0:4])-1
                    date[0] = str(year)+'-12-30'
                else:
                    if(int(date1[8:])-7 < 6):
                        date[0] = date1[0:4]+"-"+str(month)+"-30"
                    elif(int(date1[8:])-7 < 10):
                        date[0] = date1[0:4]+"-"+str(month)+"-0"+str(int(date1[8:])-7)
                    else:
                        date[0] = date1[0:4]+"-"+str(month)+str(int(date1[8:])-7)
            else:
                date[0]=date1[0:8]+str(int(date1[8:])-7)
        elif(date[0]=="Last One Month"):
            date1 = time.strftime("%Y-%m-%d")
            month = str(int(date1[5:7])-1)
            if(int(date1[5:7]) < 1):
                year = int(date1[0:4])-1
                date[0] = str(year)+'-12-'+date1[8:]
            else:
                date[0] = date1[0:4]+"-"+month+"-"+str(int(date1[8:]))
        else:
            date1 = time.strftime("%Y-%m-%d")
            year = str(int(date1[0:4])-1)
            date[0] = year+"-"+date1[5:]
        date1 = time.strftime("%Y-%m-%d")
        temp_date = date1
        date1 = date1[0:9]+str(int(date1[9:11]) + 1)
        date.append(date1)
        query = "select * from transaction where transactiondate between '"+date[0]+"' and '"+date[1]+"' and accountno='"+session['AccountNo']+"' order by transactiondate desc"
        cursor = DBConnectivity.getQueryResult(con, query)
        transaction = cursor.fetchall()
        if(len(transaction) > 0):
            return render_template("printStatement.html",transaction=transaction)
        else:
            flash("No Record found between "+date[0]+" and "+temp_date,"danger")
            return redirect(url_for('statement.getStatement'))
    