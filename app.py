from flask import Flask, render_template, request, redirect, url_for,flash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Gundu%402002@localhost/restaurants'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    query = text("SELECT * FROM user;")
    result = db.engine.execute(query)
    print(result)
    
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    city= db.Column(db.String(255), nullable=False)
    phone_no=db.Column(db.String(255), nullable=False)
class Item1(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    item_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)





with app.app_context():
    db.create_all()
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        item_amount = float(request.form['item_amount'])
        category = request.form['category']

        
        existing_item = Item1.query.filter_by(name=name).first()
        if existing_item:
            flash('Item already exists!', 'danger')
        else:
            new_item = Item1(name=name, item_amount=item_amount, category=category)
            db.session.add(new_item)
            db.session.commit()
        return redirect(url_for('add_item'))  # Redirect to the add_item page after adding the item

    return render_template('admin.html')
@app.route('/display_item')
def display_item():
    items = Item1.query.all()
    return render_template('admin.html', items=items)



@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

# @app.route('/user_login',methods=['GET', 'POST'])
# def user_login():
#     email = request.form['email']
#     password = request.form['password']
#     specific_user = db.session.query(User).filter_by(email='kgundurao09@gmail.com', password='123').first()
#     print(specific_user)
#     if specific_user:
#         return render_template('user_login.html')
#     else:
#         return redirect(url_for('user_signup'))


# @app.route('/delete_item/<int:id>', methods=['POST'])
# def delete_item(id):
#     # Delete the item from the database
#     item = Item.query.get(id)
#     if item:
#         db.session.delete(item)
#         db.session.commit()
#     return redirect(url_for('admin'))

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        specific_user = db.session.query(User).filter_by(email=email, password=password).first()
        # username= db.session.query(User.name).filter_by(name=email).first()
        
        if specific_user:
            return redirect(url_for('welcome',username=specific_user.name))

    return render_template('user_login.html')

@app.route('/welcome/<username>',methods=['GET'])
def welcome(username):
    return render_template('welcome.html',username=username)

@app.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    tasks = User.query.all()
    return render_template('user_signup.html', tasks=tasks)

@app.route('/northern_food')
def northern_food():
    items = Item1.query.with_entities(Item1.item_id, Item1.name, Item1.item_amount).filter_by(category='northern_food').all()
    return render_template('northern_food.html', items=items)

@app.route('/southern_food')
def southern_food():
    items = Item1.query.with_entities(Item1.item_id, Item1.name, Item1.item_amount).filter_by(category='southern_food').all()
    return render_template('southern_food.html', items=items)

@app.route('/snacks')
def snacks():
    return render_template('snacks.html')

@app.route('/add', methods=['POST'])
def add():
    print(request.form)  # Print form data for debugging
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        phone_no = request.form['phone_no']
        new_user = User(name=name, email=email, password=password,city=city,phone_no=phone_no)
        db.session.add(new_user)
        db.session.commit()
        
        if new_user:
            return redirect(url_for('user_login'))
        return redirect(url_for('user_signup'))
    except KeyError as e:
        return f"KeyError: {e} not found in form data."


if __name__ == '__main__':
    app.run(debug=True)
