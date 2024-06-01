from flask import Flask, render_template, request, redirect, url_for,flash
import os
from Querypart import Queries
app = Flask(__name__, template_folder=os.path.abspath('templates'))
table = Queries(dbname="trial")
@app.route('/')
def main():
    return render_template('main.html')
@app.route('/admin_contact')
def admin_contact():
    return render_template('admin_contact.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    return render_template('user_signup.html')
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        global current_user
        current_user = list(table.check_login(email,password)[0])[0]
        print(current_user)
        if current_user:
            username = list(table.get_current_user_info(current_user)[0])[0]
            return welcome(username) 
        else:
            print("Login Failed")
            return redirect(url_for('user_signup'))
    return render_template("user_login.html")
@app.route('/add',methods=['GET','POST'])
def add_order():
        quantity= request.form['quantity']
        name= request.form['name']
        print(quantity,name,current_user)
        id = int(table.chect_item_id(name)[0][0])
        print(id)
        print(type(quantity),type(name),type(id))
        table.insert_order(id,current_user,quantity)
        return render_template('index.html')
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    items = table.get_items()
    print(items)
    if request.method == 'POST':
        name = request.form['name']
        item_amount = float(request.form['item_amount'])
        category = request.form['category']
        if not table.check_item(name):
            table.insert("item",f"'{name}',{item_amount},'{category}'","name,item_amount,category")
            print("Inserted Sucessfully")
        else:
            print("Sorry the item is present...!")
        return redirect(url_for('add_item'))  # Redirect to the add_item page after adding the item

    return render_template('admin.html',items=items)

@app.route('/submit', methods=['POST'])
def submit():
    selected_option = request.form.get('radio_option')
    print("Selected: ",selected_option)
    match selected_option:
        case "northern_food":return redirect(url_for('northern_food'))
        case "southern_food":return redirect(url_for('southern_food'))
        case "snacks":return redirect(url_for('snacks'))
    return 'Check the console for the selected option'
@app.route('/welcome<username><user_id>', methods=['POST'])
def welcome(username):
    return render_template('welcome.html',username=username)

@app.route('/add_user', methods=['GET','POST'])
def add():
    print(request.form)  # Print form data for debugging
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        phone_no = request.form['phone_no']
        new_user = table.insert('User',f"'{name}','{email}','{password}','{city}','{phone_no}'","name,email,password,city,phone_no")
        if new_user:
            print("User Created")
            return redirect(url_for('user_login'))
        return redirect(url_for('user_signup'))
    except KeyError as e:
        return f"KeyError: {e} not found in form data."
@app.route('/northern_food')
def northern_food():
    items=table.northern_food()
    return render_template('northern_food.html',items=items)
@app.route('/southern_food')
def southern_food():
    items=table.southern_food()
    return render_template('southern_food.html',items=items)

@app.route('/snacks')
def snacks():
    items=table.snacks()
    return render_template('snacks.html',items=items)
@app.route('/count_details')
def count_details():
    order_count=int(table.order_count()[0][0])
    user_count=int(table.user_count()[0][0])
    item_count=int(table.item_count()[0][0])
    return render_template('count_details.html',user_count=user_count,order_count=order_count,item_count=item_count)
@app.route('/view_order')
def view_order():
    result=table.order_details_north()
    result1=table.order_details_south()
    result2=table.order_details_()
    return render_template('view_order.html',result=result,result1=result1,result2=result2)
# @app.route('/bill')
# def bill():
#     order_no=table.order_no_check()
#     print(order_no)
#     table.insert_bill(order_no)
#     return render_template('bill.html')
if __name__ == '__main__':
    app.run(debug=True)
