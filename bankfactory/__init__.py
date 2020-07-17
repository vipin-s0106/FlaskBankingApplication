from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import session

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r"D:\Programms\PythonApplication\BankApplication\bankfactory\static\profile"
app.config['SECRET_KEY'] = '125a172d79899a122269f137c78485b0'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from bankfactory.main.routes import main
from bankfactory.customer.routes import customer
from bankfactory.statement.routes import statement
from bankfactory.cards.routes import cards
from bankfactory.transfer.routes import transfer
from bankfactory.loans.routes import loans
from bankfactory.recharge.routes import recharge

app.register_blueprint(main)
app.register_blueprint(customer)
app.register_blueprint(statement)
app.register_blueprint(cards)
app.register_blueprint(transfer)
app.register_blueprint(loans)
app.register_blueprint(recharge)


