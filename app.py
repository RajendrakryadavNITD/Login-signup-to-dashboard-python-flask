from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import manipulation_of_csv_data_list , write_in_csv
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, FloatField
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

#config MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'todolist'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL(app)




@app.route('/')
def index():
	return render_template('home.html')

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=1, max=50)])
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message='PassWord do not match')
		])
	confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ['GET', 'POST'])

def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#create cursor
		cur = mysql.connection.cursor()

		#execute query
		cur.execute("insert into users (name, email, username, password) Values(%s, %s, %s, %s)",(name, email, username, password))

		#commit to DB
		mysql.connection.commit()

		#close connection
		cur.close()

		flash('you are now register and can log in', 'success')

		return redirect(url_for('index'))
		# return render_template('register.html', form = form)
	return render_template('register.html', form =form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method =='POST':
		print request.form
		username = request.form.get('username', None)
		password_candidate = request.form.get('password',None)
		print username
		print password_candidate
		#create cursor
		cur = mysql.connection.cursor()

		#get user by username
		result = cur.execute("select * from users where username=%s",[username])

		if result > 0:
			#get stored hash
			data = cur.fetchone()
			password = data['password']

			if sha256_crypt.verify(password_candidate, password):
				# app.logger.info('password matched')
				session['logged_in'] = True
				session['username'] = username

				flash('you are now logged in', 'success')
				return redirect(url_for('dashboard'))
			else:
				error = 'Invalid login/password'
				return render_template('login.html', error = error) 
			# close connection
			cur.close
		else:
			error = 'User not found'
			return render_template('login.html', error = error) 
	return render_template('login.html') 


def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('unauthorized, please login', 'danger')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('you are now logged out', 'success')
	return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
	csv_data = manipulation_of_csv_data_list()
	csv_data.reverse()
	if len(csv_data) >0:
		return render_template('dashboard.html', articles = csv_data)
	else:
		msg = 'No Articles Found'
		return render_template('dashboard.html', msg =msg)
	cur.close()


class OrderForm(Form):
	order_id = StringField('Order ID', [validators.Length(min=1, max=100)])
	product_name = StringField('Product Name', [validators.Length(min=1, max=100)])
	order_status = StringField('Order Status', [validators.Length(min=1, max=50)])
	product_url = StringField('Product Url', [validators.Length(min=1, max=500)])
	cost_price = FloatField('Cost Price',  [validators.required()])


@app.route('/add_order', methods=['GET', 'POST'])
@is_logged_in
def add_order():
	form = OrderForm(request.form)
	if request.method == 'POST':
		order_id = form.order_id.data
		product_name = form.product_name.data
		order_status = form.order_status.data
		product_url = form.product_url.data
		cost_price = form.cost_price.data

		status = write_in_csv(order_id, product_name, order_status, product_url, cost_price)


		flash('Order created', 'success')
		return redirect(url_for('dashboard'))
	return render_template('add_order.html', form =form)


if __name__ == '__main__':
	app.secret_key = 'secretkey'
	app.run(debug=True)