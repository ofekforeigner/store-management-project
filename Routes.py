from flask import Flask, render_template, request, flash, session, url_for, redirect, send_from_directory, abort
from Forms import RegisterationForm, LoginForm, TaskForm, MailForm, FlagForm, ContactForm, ItemsForm, SupplierForm
from werkzeug.security import generate_password_hash, check_password_hash
import webbrowser
import winsound
import mysql.connector
import mysql
from datetime import date
from Users import Users
from Tasks import Tasks
from Log import logs_event
from Mail import Mail_Class
from Contacts import Contacts
from Reports import Reports
from Pdf import Pdf
import itertools
import time
from Xml import Xml
from Items import Items
from Suppliers import Suppliers
from Categories import Categories
from Orders import Orders
import os
import pandas as pd
import re
from tabulate import tabulate
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

log = logs_event()

try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database="project"
    )
    log.inf_write("The system has successfully connected to the database.")
except mysql.connector.Error as error:
    log.err_write("error with connection to db")

mycursor = db.cursor()

global Users_online
Users_online = []
taskAlert = Xml().task_alert(db)
alert_value = Xml().tasks_get()
alert_counter = len(Xml().task_alert(db))
disp_mode = ["1. כל הפריטים",
             "2. פעילים", "3. לא פעילים"]

app.secret_key = "heelo"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = Xml().email_get()
app.config['MAIL_PASSWORD'] = Xml().pass_get()

######################################################
#                      Logout                        #
######################################################


# LOGOUT THE USER
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        users = Users(db, username, " ", " ")
        user = users.get_employee_by_username(username)
        if user and check_password_hash(user[0][4], password):
            session['loggedin'] = True
            session['userName'] = username
            session['isAdmin'] = users.is_admin()[0][0]
            session['name'] = users.get_employee_name_by_username(username)[
                0][0]
            Users_online.append(session['name'])
            log.inf_write("Connection with user:" +
                          users.get_employee_name_by_username(username)[0][0])
            log.query_write("SELECT * FROM employees WHERE employee_username = '" +
                            username + "' AND employee_password = ****** ")
            flash(
                f'ברוך הבא {users.get_employee_name_by_username(username)[0][0]} ', 'success')
            update_stock_after_order_closed()
            if Xml().sound_get():
                winsound.PlaySound(
                    "static/sounds/WindowsLogonSound.wav", winsound.SND_ASYNC)
            if 'loggedin' in session and session['isAdmin'] != '1':
                log.query_write("SELECT * FROM employees WHERE employee_username = '" +
                                username + "' AND employee_password = ****** ")
                log.inf_write("Connection with user:" +
                              users.get_employee_name_by_username(username)[0][0])
                session['thisPage'] = "employeehome.html"
                return redirect(url_for('employee_home'))
            session['thisPage'] = "home.html"
            return redirect(url_for('home'))
        else:
            session['loggedin'] = False
            flash('ההתחברות נכשלה, בדוק את שם המשתמש והסיסמה',
                  'danger')
            log.query_write("SELECT * FROM employees WHERE employee_username = '" +
                            username + "' AND employee_password = ****** ")
            log.inf_write("Incorrect password or username")
    return render_template('login.html', title='התחברות', form=form)


# UPDATE THE STOCK WHEN ORDERS ARE IN CURRENT DATE
def update_stock_after_order_closed():
    orders_numbers = Orders(db).get_orders_number_by_order_checked_status()
    orders_numbers_return_to_supplier = Orders(
        db).get_orders_number_by_order_checked_status_expired_items()
    expired_orders = Orders(db).get_expired_orders_number()
    Orders(db).show_order_quantity_by_id(orders_numbers)
    Orders(db).close_order_by_type(orders_numbers)
    Orders(db).close_order_by_type(orders_numbers_return_to_supplier)
    Orders(db).close_expired_orders(expired_orders)


# POP UP THE USER FROM THE SESSION
@app.route("/login")
def logout():
    log.inf_write("Page.Init completed - Login Page.")
    log.inf_write("logout success")
    if Xml().sound_get():
        winsound.PlaySound(
            "static/sounds/WindowsLogoffSound.wav", winsound.SND_ASYNC)
    flash("התנתקת בהצלחה!", "success")
    try:
        Users_online.pop(Users_online.index(session['name']))
        session.pop('name', None)
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - Login Page.")
        log.err_write("error:   " + str(error.__doc__))
    session.pop('loggedin', None)
    session.pop('userName', None)
    return redirect(url_for('login'))


######################################################
#                      Home                          #
######################################################


# DISPLAY THE MANAGER HOME PAGE
@ app.route("/home")
def home():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - home Page.")
            ct = Tasks(db, "", "", "",
                       "").count_completed_tasks_for_dashboard()  # get the number of completed tasks for the dashboard panel
            active_users = Users(db, "", "", "").count_employees()
            checked_orders = Orders(db).count_checked_orders()
            return render_template('home.html', title='דף הבית', logged_user=session['name'], users=Users_online, taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), advert=Xml().advert_get(), business=Xml().business_details_get(), alert_counter=len(Xml().task_alert(db)), itemsAlert=Xml().items_date_alert(db), items_value=Xml().items_get(), items_amount=Xml().items_amount_alert(db), items_amount_alert=Xml().items_value_amount_get(), ct=ct, active_users=active_users, checked_orders=checked_orders)
        else:
            log.inf_write("Page.Init failed - home Page.")
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - home Page.")
        log.err_write("error:   " + str(error.__doc__))


# DISPLAY THE EMPLOYEE HOME PAGE
@ app.route("/employee_home")
def employee_home():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - employee_home Page.")
            return render_template('employeehome.html', title='דף הבית', logged_user=session['name'], tasks=Tasks(db, "", "", "", "").get_all_tasks(), taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), advert=Xml().advert_get(), business=Xml().business_details_get(), alert_counter=len(Xml().task_alert(db)), itemsAlert=Xml().items_date_alert(db), items_value=Xml().items_get(), items_amount=Xml().items_amount_alert(db), items_amount_alert=Xml().items_value_amount_get())
        else:
            log.inf_write("Page.Init failed - employee_home Page.")
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - employee_home Page.")
        log.err_write("error:   " + str(error.__doc__))

######################################################
#                      Orders                        #
######################################################


# DISPLAY ALL ORDERS
@ app.route("/orders")
def orders():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - orders Page.")
            return render_template("orders.html", title='הזמנות', suppliers=Suppliers(db).get_suppliers(), suppliers_name=Suppliers(db).get_supplier_names(), orders=Orders(db).get_orders(), taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)), types=["הזמנה מספק", "החזרת סחורה לספק"], logged_user=session['name'])
        else:
            log.inf_write("Page.Init failed - orders Page.")
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - orders Page.")
        log.err_write("error:   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))


# CREATE NEW ORDER FROM A SPECIFIC SUPPLIER


@ app.route("/add_order", methods=['GET', 'POST'])
def add_order():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                if request.args:
                    order_name = request.args.get('name')
                    supplier_mail = Orders(
                        db).get_supplier_mail_by_supplier_name(order_name)
                    Orders(db).add_new_order(
                        order_name, supplier_mail, request.args.get('date'), request.args.get('type'), 0)
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.inf_write("order: " + order_name +
                                  " added to database.")
                    return redirect(url_for('orders'))
                return redirect(url_for('orders'))
            return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("add order failed.")
        log.err_write("error:   " + str(error.__doc__))
        flash('שגיאה !', 'danger')
        return redirect(url_for('home'))


# CREATE NEW ORDER OF EXPIRED ITEMS FROM THE HOME PAGE


@ app.route("/add_expired_items_order_from_home_page", methods=['GET', 'POST'])
def add_expired_items_order_from_home_page():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                supplier_name = request.args.get('supplier_name')
                item_data = request.args.getlist('item_data[]')
                barcodes = [barcode.split("#")[0] for barcode in item_data]
                item_id = [item_id.split("#")[1] for item_id in item_data]
                supplier_mail = Orders(
                    db).get_supplier_mail_by_supplier_name(supplier_name)
                Orders(db).add_new_order(supplier_name, supplier_mail, request.args.get(
                    'date'), request.args.get('type'), 0)
                order_number = Orders(db).get_last_inserted_order_id()
                Orders(db).add_item_to_order_by_barcode(
                    barcodes, order_number[0][0])
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                Orders(db).reset_items_quantity_after_return_to_supplier(item_id)
                log.inf_write("order: " + supplier_name +
                              " added to database.")
                return redirect(url_for('home'))
            return redirect(url_for('home'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("add order failed.")
        log.err_write("error:" + "   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))

# CREATE NEW ORDER OF OUT OF STOCK ITEMS FROM THE HOME PAGE


@ app.route("/add_out_of_stock_order_from_home_page", methods=['GET', 'POST'])
def add_out_of_stock_order_from_home_page():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                supplier_name = request.args.get('supplier_name')
                item_data = request.args.getlist('item_data[]')
                barcodes = [barcode.split("#")[0] for barcode in item_data]
                quantity = request.args.get('quantity')
                supplier_mail = Orders(
                    db).get_supplier_mail_by_supplier_name(supplier_name)
                Orders(db).add_new_order(
                    supplier_name, supplier_mail, request.args.get('date'), request.args.get('type'), quantity)
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                order_number = Orders(db).get_last_inserted_order_id()
                ordernumber = order_number[0][0]
                Orders(db).add_oos_item_to_order_by_barcode(
                    barcodes, ordernumber, quantity)
                log.inf_write("order: " + supplier_name +
                              " added to database.")
                return redirect(url_for('home'))
            return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("add order failed.")
        log.err_write("error:" + "   " + str(error.__doc__))
        flash('שגיאה !', 'danger')
        return redirect(url_for('home'))
# DELETE A SPECIFIC ORDER


@ app.route("/delete_order", methods=['GET', 'POST'])
def delete_order():  # delete a specisfic user
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                if 'orderId' in request.args:
                    order_id = request.args.get('orderId')
                    if Orders(db).show_order_info_by_id(order_id):
                        log.inf_write(
                            "delete order failed. - cannot remove order with items.")
                        return redirect(url_for('orders'))
                    elif not Orders(db).show_order_info_by_id(order_id):
                        Orders(db).delete_order(order_id)
                        if Xml().sound_get():
                            winsound.PlaySound(
                                "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                        log.query_write("DELETE FROM orders WHERE order_id=")
                        log.inf_write("delete order succses.")
                        log.inf_write(
                            "order number: " + order_id + " deleted from the database.")
            return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error :   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))


"""
This function removes a certain item from the order selected by the user after we have deleted the item
we call another function that will update the total amount of the order and sum.
"""

# DELETE AN ITEM FROM ORDER


@ app.route("/delete_item_from_order", methods=['GET', 'POST'])
def delete_item_from_order():  # delete a specisfic user
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                item_id = request.args.get('itemid')
                ordernumber = request.args.get('ordernumber')
                Orders(db).remove_item_from_order(ordernumber, item_id)
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.query_write(
                    "DELETE FROM ordersitems WHERE ordersitems_id = id AND order_id = orderid")
                log.inf_write("item : " + item_id + " from order number: " +
                              ordernumber + " deleted from the database.")
                return render_template("order_info.html", title=' פרטי הזמנה', order_info=Orders(db).show_order_info_by_id(ordernumber))
            else:
                flash('אנא התחבר קודם!', 'danger')
                return redirect(url_for('login'))
        except Exception as error:
            if Xml().sound_get():
                winsound.PlaySound(
                    "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
            log.inf_write("delete item from order failed.")
            log.err_write("error " + str(error.__doc__))
            flash('שגיאה !', 'danger')
            return redirect(url_for('home'))


"""
When a user clicks on a (פרטי הזמנה) btn we use
this function to get the order ID.
ONCE WE GET AN ID WE SEND IT TO show_order_info()
"""

# DISPLAY A SPECIFIC ORDER INFO BY ORDER NUMBER


@ app.route("/get_order_info", methods=['GET', 'POST'])
def get_order_info():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                ordernumber = request.args.get('ordernumber')
                order_info = Orders(db).show_order_info_by_id(ordernumber)
                is_checked = Orders(db).get_order_checked_status(ordernumber)
                log.query_write(
                    "SELECT * from ordersItems where order_id = " + ordernumber)
                return render_template("order_info.html", title='פרטי הזמנה', is_checked=is_checked, order_info=order_info, ordernumber=ordernumber, taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)), logged_user=session['name'])
            return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("failed get order info.")
        log.err_write("error:" + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))


"""
After we have received the order number from fucntion (get_order_info)
we send it to the order page to link the items to display by order number.
"""


"""
ON CLICK (הוספת פריטים) IN orders.html WE GET THE ORDER NUMBER AND SUPPLIER NAME AND CALL
show_items_by_supplier_to_add_to_order
"""

# DISPLAY THE EXPIRED ITEMS OF A SPECIFIC SUPPLIER


@ app.route("/show_expired_items_by_supplier/<supplier>/<ordernumber>", methods=['POST', 'GET'])
def show_expired_items_by_supplier(supplier, ordernumber):
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                items = Orders(db).show_expired_items_by_supplier(supplier)
                log.query_write("SELECT * from items WHERE supplier_name = " + supplier +
                                " AND status = 1 AND experation_date <= CURRENT_DATE() AND amount > 0")
                log.inf_write(
                    "Page.Init sucsees - show_expired_items_by_supplier Page.")
                return render_template("show_items_by_supplier.html", title='הוספת פריטים להזמנה', logged_user=session['name'],
                                       items=items, order_type_table_col=0, ordernumber=ordernumber, taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
            else:
                return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        log.inf_write(
            "Page.Init failed - show_expired_items_by_supplier Page.")
        log.err_write("error  " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))
# DISPLAY ITEMS BY SUPPLIER


@ app.route("/show_items_by_supplier/<supplier>/<ordernumber>", methods=['POST', 'GET'])
def show_items_by_supplier(supplier, ordernumber):
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                return render_template("show_items_by_supplier.html", title='הוספת פריטים להזמנה', logged_user=session['name'], items=Orders(db).show_items_by_supplier(supplier), order_type_table_col=1, ordernumber=ordernumber, taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
            return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write(
            "Page.Init failed - show_items_by_supplier Page.")
        log.err_write("error  " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))


"""
ON CLICK (הוספת פריט) IN PAGE add_items_to_order.html WE ADD THE ITEM TO ordersitems TABLE ACCORDING
TO THE ORDER NUMBER OF THE ORDER WE CLICKED ON BEFORE
"""

# GET THE ORDER NUMBER AND ADD AN ITEM TO THE ORDER


@ app.route("/add_item_to_order/<ordernumber>", methods=['POST', 'GET'])
def add_item_to_order(ordernumber):
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                if 'loggedin' in session:
                    log.inf_write(
                        "Page.Init success - add_item_to_order Page.")
                    item_id = request.args.get('itemid')
                    quantity = request.args.get('quantity')
                    decExpItemQuantity = request.args.get(
                        'decExpItemQuantity')
                    if decExpItemQuantity == 'true':
                        Orders(db).reset_items_quantity_after_return_to_supplier(
                            item_id)
                    items = Items(db, "", "", "",
                                  "", "", "", "", "", "")
                    item = items.get_items_by_id(item_id)
                    Orders(db).add_item_into_order_by_order_number(
                        item, ordernumber, quantity)
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.query_write(
                        "INSERT INTO ordersitems(order_id,item_name,item_code,quantity,piece_price,price)")
                    return redirect(url_for('orders'))
                return redirect(url_for('orders'))
        else:
            log.inf_write("Page.Init failed - add_item_to_order Page.")
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - add_item_to_order Page.")
        log.err_write("error :" + "   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))


def divide_chunks(l, n):  # SPLIT THE ITEMS ARRAY INTO PAIRS OF ITEM NAME AND QTY
    for i in range(0, len(l), n):
        yield l[i:i + n]


def replace_selected_chars(a):
    a = '\n'.join([str(i) for i in a])
    vowels = "[',]"
    for i in vowels:
        a = a.replace(i, ' ')
    return a


@app.route("/check_order/<ordernumber>", methods=['POST', 'GET'])
def check_order(ordernumber):
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                ordernumber = re.split("[<>]", ordernumber)[1]
                Orders(db).approve_order_chekced_status(ordernumber)
                # send mail to supplier after click check order.
                supplier_mail = request.args.get('mail')
                order_type = request.args.get('order_type')
                items_in_order = Orders(
                    db).show_order_name_and_quantity_by_id(ordernumber)

                # SPLIT THE ITEMS ARRAY INTO PAIRS OF ITEM NAME AND QTY
                x = list(divide_chunks(items_in_order, 3))
                x = tabulate(
                    x, headers=["שם פריט", 'מק"ט', "כמות"], tablefmt='plain')
                order_date = " לתאריך ה " + \
                str(Orders(db).get_order_info_by_id(ordernumber)[0][4])
                if order_type == 'הזמנה מספק':
                    header = " הזמנת סחורה מספר " + str(ordernumber) + order_date
                else:
                    header = " החזרת סחורה מספר " + str(ordernumber) + order_date
                app.config['MAIL_USERNAME'] = Xml().email_get()
                app.config['MAIL_PASSWORD'] = read_email_encrypted_password(Xml().pass_get())
                mail = Mail_Class(db, app, header, x, supplier_mail)
                mail.send_mail()
                log.inf_write("Mail successfully sent to "+supplier_mail)
                update_stock_after_order_closed()
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.query_write(
                    "UPDATE orders SET order_checked = 1 WHERE order_id = ordernumber")
                log.inf_write("orders: " + ordernumber +
                              " updated.")
                return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("send mail failed")
        log.err_write("error   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))


@app.route("/cancel_check_order/<ordernumber>", methods=['POST', 'GET'])
def cancel_check_order(ordernumber):
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                ordernumber = re.split("[<>]", ordernumber)[1]
                Orders(db).cancel_order_chekced_status(ordernumber)
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.query_write(
                    "UPDATE orders SET order_checked = 0 WHERE order_id = ordernumber")
                log.inf_write("orders: " + ordernumber +
                              " updated.")
                return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))


@app.route("/close_order/<ordernumber>", methods=['POST', 'GET'])
def close_order(ordernumber):
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                ordernumber = re.split("[<>]", ordernumber)[1]
                Orders(db).close_order(ordernumber)
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.query_write(
                    "UPDATE orders SET order_checked = 2 WHERE order_id = ordernumber")
                log.inf_write("orders: " + ordernumber +
                              " updated.")
                return redirect(url_for('orders'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))
######################################################
#                      Categories                    #
######################################################

# DISPLAY ALL CATEGORIES


@ app.route("/categories")
def categories():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init success - categories Page.")
            return render_template("Categories.html", title='קטגוריות', logged_user=session['name'],
                                   categories=Categories(db, "").get_categories(), taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)), i=0, count=0)
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - categories Page.")
        log.err_write("error :   " + str(error.__doc__))
        flash('שגיאה !', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))
# ADD NEW CATEGORY


@ app.route("/add_category", methods=['GET', 'POST'])
def add_category():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                if request.args:
                    category_name = request.args.get('name')
                    Categories(db, category_name).add_category()
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.query_write(
                        "INSERT INTO categories(Category_name,status)")
                    log.inf_write("category: " + category_name +
                                  " add to database.")
                    return redirect(url_for('categories'))
                return redirect(url_for('categories'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - add_category Page.")
        log.err_write("error   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))

# EDIT A SPECIFIC CATEGORY


@ app.route("/edit_category", methods=['GET', 'POST'])
def edit_category():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                if request.args:
                    name = request.args.get('name')
                    Categories(db, name).edit_category(
                        request.args.get('id'))

                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.inf_write("Page.Init success - categories Page.")
                    log.query_write(
                        "UPDATE categories SET category_name = %s WHERE category_id = %s")
                    log.inf_write("category: " + name + " updated.")
                    return redirect(url_for('categories'))
            return redirect(url_for('categories'))
        else:
            log.inf_write("must login first.")
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - categories Page.")
        log.err_write("error with categories page:   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))
# CHANGE CATEGORY STATUS, ACTIVE OR INACTIVE


@ app.route("/change_category_status", methods=['GET', 'POST'])
def change_category_status():
    try:
        if request.method == 'GET':
            if request.args:
                id = request.args.get('id')
                status = request.args.get('status')
                Categories(db, "").change_category_status(id, status)
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.query_write(
                    "UPDATE categories SET status = %s WHERE Category_id = %s")
                log.inf_write("category status updated.")
                return redirect(url_for('categories'))
        return redirect(url_for('categories'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - categories Page.")
        log.err_write("error :   " + str(error.__doc__))
        flash('שגיאה !', 'danger')
        return redirect(url_for('home'))
######################################################
#                      Suppliers                     #
######################################################

# DISPLAY ALL SUPPLIERS


@ app.route("/suppliers", methods=['GET', 'POST'])
def suppliers():
    try:
        if 'loggedin' in session:
            suppliers = Suppliers(db).get_suppliers()
            log.inf_write("Page.Init success - suppliers Page.")
            return render_template("Suppliers.html", title='ספקים', logged_user=session['name'],
                                   suppliers=suppliers, taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)), display_mode=disp_mode)
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - suppliers Page.")
        log.err_write("error :   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))

# ADD NEW SUPPLIER


@ app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    try:
        form = SupplierForm()
        if 'loggedin' in session:
            if form.validate_on_submit():
                if Suppliers(db).add_supplier(form.name.data, form.phone.data, form.mail.data):
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.inf_write("new supplier created")
                    log.query_write(
                        "INSERT INTO suppliers(supplier_name,phone_number) VALUES(%s,%s)")
                    flash(f'ספק {form.name.data} נוצר בהצלחה', 'success')
                    return redirect(url_for('suppliers'))
                else:
                    flash('לא ניתן להוסיף ספק, ספק קיים במערכת', 'danger')
            return render_template('addSupplier.html', title='ספקים', form=form, logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error with add_supplier page:   " + str(error.__doc__))
        flash('שגיאה !', 'danger')
        return redirect(url_for('home'))
# EDIT A SPECIFIC SUPPLIER


@ app.route("/edit_supplier", methods=['GET', 'POST'])
def edit_supplier():
    try:
        if request.method == 'GET':
            if request.args:
                name = request.args.get('name')
                phone = request.args.get('phone')
                mail = request.args.get('mail')

                Suppliers(db).edit_supplier(
                    request.args.get('id'), name, phone, mail)
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.query_write(
                    "UPDATE suppliers SET supplier_name = %s, phone_number = %s WHERE supplier_id = %s")
                log.inf_write(
                    "supplier: " + name + " edit in database.")
                return redirect(url_for('suppliers'))
        return redirect(url_for('suppliers'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error with edit_supplier page:   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))
# CHANGE SUPPLIER STATUS, ACTIVE OR INACTIVE


@ app.route("/change_supplier_status", methods=['GET', 'POST'])
def change_supplier_status():
    try:
        if request.method == 'GET':
            id = request.args.get('id')
            status = request.args.get('status')
            suppliers = Suppliers(db)
            suppliers.change_supplier_status(id, status)
            if Xml().sound_get():
                winsound.PlaySound(
                    "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
            return redirect(url_for('suppliers'))
        return redirect(url_for('suppliers'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write(
            "error with change_supplier_status page:  " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))
######################################################
#                      Items                         #
######################################################

# DISPLAY ALL ITEMS


@ app.route("/items")
def items():
    try:
        if 'loggedin' in session:
            items = Items(db, "", "", "", "", "", "", "", "", "")
            item = items.get_items()
            m_units = ['ק"ג', "יחידות"]
            log.inf_write("Page.Init completed - items Page.")
            return render_template("items.html", exp_date=date.today(), logged_user=session['name'], items_amount=Xml().items_amount_alert(db), items_amount_alert=Xml().items_value_amount_get(), itemsAlert=Xml().items_date_alert(db), items_value=Xml().items_get(), title='פריטים', items=item, suppliers=Suppliers(db).get_supplier_names(), categories=Categories(db, "").get_category_names(), suppliers_full_data=Suppliers(db).get_suppliers, m_units=m_units, taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - items Page.")
        log.err_write("error :   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))

# ADD NEW ITEM


@ app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    try:
        form = ItemsForm()
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - items Page.")
            supplier = Suppliers(db)
            categories = Categories(db, "")
            names_list = supplier.get_supplier_names()
            form.supplier.choices = [(name, name) for name in names_list]
            form.unit_of_measurment.choices = ['ק"ג', "יחידות"]
            names_list = categories.get_category_names()
            form.category.choices = [(name, name) for name in names_list]
            if form.validate_on_submit():
                items = Items(db, form.name.data, form.catalogue_number.data, form.amount.data,
                              form.buy_price.data,
                              form.sell_price.data, form.experation_date.data, form.category.data,
                              form.unit_of_measurment.data, form.supplier.data)
                if items.add_item():
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.query_write(
                        "INSERT INTO items(catalogue_number, item_name, amount, buy_price, sell_price, experation_date, category, unit_of_measurment, supplier_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    log.inf_write(
                        "new item add - name:" + form.name.data)
                    flash(f'!פריט {form.name.data} נוצר בהצלחה', 'success')
                    return redirect(url_for('items'))
                else:
                    flash('לא ניתן להוסיף פריט, פריט קיים במערכת', 'danger')
            return render_template('addItem.html', title='פריטים', form=form, logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - items Page.")
        log.err_write("error    " + str(error.__doc__))
        flash('שגיאה !', 'danger')
        return redirect(url_for('home'))
# EDIT A SPECIFIC ITEM


@ app.route("/edit_item", methods=['GET', 'POST'])
def edit_item():  # edit a specific item
    try:
        if request.method == 'GET':
            name = request.args.get('name')
            baracod = request.args.get('barcode')
            quantity = request.args.get('quantity')
            buy_price = request.args.get('buyPrice')
            sell_price = request.args.get('sellPrice')
            exp_date = request.args.get('experationDate')
            category = request.args.get('category')
            supplier = request.args.get('supplier')
            m_unit = request.args.get('unitOfMeasurment')
            items = Items(db, name, baracod, quantity, buy_price,
                          sell_price, exp_date, category, m_unit, supplier)
            items.edit_item(request.args.get('id'))
            if Xml().sound_get():
                winsound.PlaySound(
                    "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
            log.query_write(
                "UPDATE items SET item_name = %s, catalogue_number = %s, amount = %s, buy_price = %s, sell_price = %s, supplier_name = %s, experation_date = %s, category = %s, unit_of_measurment = %s WHERE item_id = %s")
            log.inf_write("item: " + name + " edit in database.")
            return redirect(url_for('items'))
        return redirect(url_for('items'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("edit item - failed.")
        log.err_write("error" + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))
# DISPLAY ALL ITEMS THAT ARE OUT OF STOCK


@ app.route("/outofstock")
def outofstock():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - outofstock Page.")
            item = Xml().items_amount_alert(db)
            return render_template("outofstock.html", title='גמר מלאי', items=item,
                                   suppliers=Suppliers(
                                       db).get_supplier_names(),
                                   categories=Categories(
                                       db, "").get_category_names(),
                                   suppliers_full_data=Suppliers(db).get_suppliers, logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - outofstock Page.")
        log.err_write("error with outofstock page:   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))
# DISPLAY ALL EXPIRED ITEMS


@ app.route("/expired_items")
def expired_items():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - expired_items Page.")
            items = Items(db, "", "", "", "", "", "", "", "", "")
            return render_template("expired_items.html", title='פגי תוקף', logged_user=session['name'], items=items.show_expired_items(), suppliers=Suppliers(db).get_supplier_names(), categories=Categories(db, "").get_category_names(), suppliers_full_data=Suppliers(db).get_suppliers(), taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - expired_items Page.")
        log.err_write("error with expired items page:   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))
# CHANGE ITEM STATUS, ACTIVE OR INACTIVE


@ app.route("/change_item_status", methods=['GET', 'POST'])
def change_item_status():
    try:
        if request.method == 'GET':
            if request.args:
                id = request.args.get('id')
                status = request.args.get('status')
                Items(db, "", "", "",
                      "", "", "", "", "", "").change_item_status(id, status)
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                return redirect(url_for('items'))
        return redirect(url_for('items'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error with change item status:   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))
######################################################
#                      Employees                     #
######################################################

# DISPLAY ALL EMPLOYEES INFORMATION


@ app.route('/employeesInformation', methods=['GET', 'POST'])
def employees_data():
    try:
        if 'loggedin' in session:
            users = Users(db, " ", " ", " ")
            log.inf_write("Page.Init completed - employeesInformation Page.")
            return render_template("employeesInformation.html", title='עובדים', logged_user=session['name'],
                                   value=users.get_employees(),
                                   taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - employeesInformation Page.")
        log.err_write("error :   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))

# ADD NEW EMPLOYEE


@ app.route('/addEmployee', methods=['GET', 'POST'])
def add_employee():
    try:
        form = RegisterationForm()
        if 'loggedin' in session:
            log.inf_write("Page.Init success - addEmployee Page.")
            if form.validate_on_submit():
                users = Users(db, form.username.data,
                              form.name.data, str(form.isAdmin.raw_data[0]))
                if users.check_if_user_exists():
                    log.inf_write(
                        "new user added - name:" + form.name.data)
                    log.query_write(
                        "SELECT * FROM employees WHERE employee_username = '" + form.username.data + "'")
                    users.user_register(generate_password_hash(
                        form.password.data))
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.inf_write(
                        "INSERT INTO employees(employee_username, employee_password, employee_name, employee_role) VALUES(%s,%s,%s,%s)")
                    flash(
                        f'!המשתמש {form.username.data} נוצר בהצלחה', 'success')  # shows a success register message
                    log.inf_write(
                        "Page.Init completed - employeesInformation Page.")
                    return redirect(url_for('employees_data'))
                else:
                    flash('נסה שם משתמש אחר או בדוק את הנתונים!', 'danger')
                    log.inf_write("Register failed.")
            return render_template('addEmployee.html', title='עובדים', form=form, logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init success - addEmployee Page.")
        log.err_write("error with addEmployee:" + "   " + str(error.__doc__))
        flash('שגיאה!', 'danger')
        return redirect(url_for('home'))
# EDIT A SPECIFIC EMPLOYEE


@ app.route("/editUser", methods=['GET', 'POST'])
def edit_user():
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                if request.args:
                    name = request.args.get('name')
                    users = Users(db, request.args.get(
                        'userName'), name, " ")

                    users.edit_user(request.args.get('userId'))
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.inf_write(
                        "user : " + name + " edited successfully.")
                    return redirect(url_for('employees_data'))
            return redirect(url_for('employees_data'))
        except Exception as error:
            log.err_write("error  with employee data:" +
                          "   " + str(error.__doc__))
            flash('שגיאה!', 'danger')
            return redirect(url_for('home'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))

# CHANGE EMPLOYEE STATUS TO ACTIVE/INACTIVE


@ app.route("/change_employee_status", methods=['GET', 'POST'])
def change_employee_status():
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                if request.args:
                    id = request.args.get('id')
                    status = request.args.get('status')
                    Users(db, "", "", "").change_employee_status(id, status)
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    return redirect(url_for('employees_data'))
            return redirect(url_for('employees_data'))
        except Exception as error:
            log.err_write("error with change_employee_status:" +
                          "   " + str(error.__doc__))
            flash('שגיאה !', 'danger')
            return redirect(url_for('home'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))


# PATH TO THE FOLDER WHERE THE WORK SCHEDULES ARE SAVED
app.config["SHIFT_UPLOADS"] = "static/shifts/uploads/"
app.config["ALLOWES_SHIFT_EXTENSIONS"] = [
    "XLSX"]  # THE ALLOWED EXTENSIONS OF THE WORK SCHEDULE FILE
app.config['MAX_CONTENT_FILESIZE'] = 50 * 1024 * \
    1024  # THE SIZE OF THE WORK SCHEDULE FILE (50MB)

# CHECKS THE FILE EXTENSION


def allowed_content(filename):
    if 'loggedin' in session:
        try:
            if not "." in filename:
                return False
            ext = filename.rsplit(".", 1)[1]
            if ext.upper() in app.config["ALLOWES_SHIFT_EXTENSIONS"]:
                return True
            else:
                return False
        except Exception as error:
            log.err_write("error with allowed_content:" +
                          "   " + str(error.__doc__))
            flash('שגיאה', 'danger')
            return redirect(url_for('home'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))

# CHECKS THE FILE SIZE


def allowed_content_filesize(filesize):
    if 'loggedin' in session:
        try:
            if int(filesize) <= app.config["MAX_CONTENT_FILESIZE"]:
                return True
            else:
                return False
        except Exception as error:
            log.err_write("error with allowed_content_filesize:" +
                          "   " + str(error.__doc__))
            flash('שגיאה', 'danger')
            return redirect(url_for('home'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))

# UPLOAD THE WORK SCHEDULE FILE


@ app.route("/work_schedule", methods=["GET", "POST"])
def work_schedule():
    if 'loggedin' in session:
        if request.method == "POST":
            if request.files:
                if "filesize" in request.cookies:
                    if not allowed_content_filesize(request.cookies["filesize"]):
                        flash("קובץ גדול מדי!", "danger")
                        return redirect(request.url)
                    ws = request.files["ws"]
                    if ws.filename == "":
                        flash("לא נבחר קובץ!", "danger")
                        return redirect(request.url)
                    if allowed_content(ws.filename):
                        ws.save(os.path.join(
                            app.config["SHIFT_UPLOADS"], ws.filename))
                        if Xml().sound_get():
                            winsound.PlaySound(
                                "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                        flash("הקובץ הועלה בהצלחה!", "success")
                        return redirect(request.url)
                    else:
                        flash("פורמט קובץ לא תקין!", "danger")
                        return redirect(request.url)
        return render_template("work_schedule.html", files=os.listdir(
            app.config["SHIFT_UPLOADS"]), logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))

# GETS THE FILE NAME OF THE WEEKLY SHIFTS AND DISPLAY IT


@ app.route("/weekly_shifts/<filename>", methods=["GET", "POST"])
def weekly_shifts(filename):
    if 'loggedin' in session:
        if request.method == "GET":
            data = pd.read_excel(app.config["SHIFT_UPLOADS"]+filename)
            return render_template("weekly_shifts.html", data=data.to_html(), logged_user=session['name'])
        return redirect(url_for('work_schedule'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))
# GETS THE FILE NAME FROM THE URL THROUGH JQUERY AND SEND IT TO get_file METHOD


@ app.route('/get_file_name', methods=["GET", "POST"])
def get_file_name():
    if 'loggedin' in session:
        if request.method == 'GET':
            if request.args:
                try:
                    filename = request.args.get('filename')
                    return redirect(url_for('get_file', file_name=filename))
                except FileNotFoundError:
                    abort(404)
        return redirect(url_for('work_schedule'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))
# GETS THE FILE NAME FROM get_file_name AND DOWNLOAD THE FILE


@ app.route('/get-file/<file_name>', methods=["GET", "POST"])
def get_file(file_name):
    if 'loggedin' in session:
        try:
            return send_from_directory(app.config["SHIFT_UPLOADS"], filename=file_name, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))

######################################################
#                      Reports                       #
######################################################


try:
    app.config["REPORTS"] = "reports/"
except Exception as error:
    if Xml().sound_get():
        winsound.PlaySound(
            "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
    log.err_write("error with reports dir:   " + str(error.__doc__))

# DOWMLOAD REPORT


@  app.route("/download_reports", methods=["GET", "POST"])
def download_reports():
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                if request.args:
                    report_format = request.args.get('id')  # get report id
                    if not request.args.get('orderId'):
                        order_id = ""
                    else:
                        order_id = request.args.get('orderId')
                    if not request.args.get('start'):
                        start_date = ""
                    else:
                        start_date = request.args.get('start')
                    if not request.args.get('end'):
                        end_date = ""
                    else:
                        end_date = request.args.get('end')  # get report id
                    if report_format == '1':
                        items = Items(db, "", "", "", "", "", "",
                                      "", "", "").print_all_items_in_pdf()
                        total_items = Items(db, "", "", "", "", "",
                                            "", "", "", "").items_quantity()
                        pdf = Pdf(1, "דוח_מלאי_פריטים",
                                  ':יאלמב םיטירפ כ"הס', "", "")
                        pdf.items_in_stock_to_pdf(items, total_items)
                        pdf.save_pdf()
                    if report_format == '2':
                        items = Items(db, "", "", "", "", "", "", "", "",
                                      "").print_expired_items_in_pdf(start_date, end_date)
                        total_items = Items(
                            db, "", "", "", "", "", "", "", "", "").get_quntity_of_expired_items(start_date, end_date)
                        pdf = Pdf(2, "פריטים_פגי_תוקף",
                                  ': ףקות יגפ  םיטירפ כ"הס', start_date, end_date)
                        pdf.items_in_stock_to_pdf(items, total_items)
                        pdf.save_pdf()
                    if report_format == '3':
                        # get amount to query to get result
                        items_value_condtion = Xml().items_amount_get()
                        items = Items(db, "", "", "", "", "", "", "", "",
                                      "").print_all_ItemsAmount_in_pdf(items_value_condtion)
                        total_items = Items(db, "", "", "", "", "", "", "", "",
                                            "").get_quntity_of_ItemsAmount(items_value_condtion)
                        pdf = Pdf(2, "גמר_מלאי_פריטים",
                                  ':יאלמ רמגב םיטירפ כ"הס', "", "")
                        pdf.items_in_stock_to_pdf(items, total_items)
                        pdf.save_pdf()
                    if report_format == '4':  # categories
                        categories = Categories(db, "").get_categories_to_pdf()
                        total_categories = Categories(
                            db, "").get_quntity_of_categories()
                        pdf = Pdf(2, "רשימת_קטגוריות",
                                  ': תוירוגטק כ"הס', "", "")
                        pdf.categories_to_pdf(categories, total_categories)
                        pdf.save_pdf()
                    if report_format == '5':
                        items = Orders(db).get_top_5_sold_items_report(
                            start_date, end_date)
                        pdf = Pdf(2, "פריטים_מצטיינים",
                                  "", "", "")
                        pdf.top_5_sold_items(items)
                        pdf.save_pdf()
                    if report_format == '6':
                        order_info = Orders(db).get_order_info_by_id(order_id)
                        order_items_info = Orders(
                            db).show_order_info_by_id_to_report(order_id)
                        supplier_name = order_info[0][1]
                        if " " in supplier_name:
                            supplier_name = supplier_name.replace(" ", "-")
                        pdf = Pdf(2, "דוח_הזמנה_מספר_" + str(order_id)+"_מ"+supplier_name,
                                  ':הנמזהב םיטירפ כ"הס', "", "")
                        pdf.order_by_supplier(order_info, order_items_info)
                        pdf.save_pdf()
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    return redirect(url_for('reports'))
            return render_template("reports.html", reports_list=Reports(db).show_reports_types(), title='דוחות', logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        except Exception as error:
            if Xml().sound_get():
                winsound.PlaySound(
                    "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
            log.err_write("error with reports:   " + str(error.__doc__))
            flash('שגיאה', 'danger')
            return redirect(url_for('home'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))
# DISPLAY ALL DOWNLOADED REPORTS FOM reports FOLDER


@ app.route("/downloaded_reports_list/", methods=["GET", "POST"])
def downloaded_reports_list():
    if 'loggedin' in session:
        try:
            if request.method == 'GET':
                dates = []
                files = os.listdir(app.config["REPORTS"])
                path = os.getcwd()+"//"+app.config["REPORTS"]
                files.sort(key=lambda f: os.path.getmtime(
                    os.path.join(path, f)), reverse=True)
                for file in files:
                    dates.append(time.ctime(os.path.getctime(path+file)))
                log.inf_write(
                    "Page.Init success - downloaded_reports_list Page.")
                return render_template("downloaded_reports_list.html", filenames=files, dates=dates, i=0, logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        except Exception as error:
            log.inf_write("Page.Init failed - downloaded_reports_list Page.")
            log.err_write("error with downloaded_reports_list   " +
                          str(error.__doc__))
            flash('שגיאה', 'danger')
            return redirect(url_for('home'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))
# GETS THE REPORT NAME AND DISPLAY IT


@ app.route('/display_report/<filename>')
def display_report(filename):
    if 'loggedin' in session:
        try:
            file_name = re.split("[<>]", filename)
            path = os.getcwd()
            webbrowser.open_new_tab(path + '//reports//' + file_name[1])
            return redirect(url_for('downloaded_reports_list'))
        except Exception as error:
            log.err_write("error with display_report:" +
                          "   " + str(error.__doc__))
            flash('שגיאה', 'danger')
            return redirect(url_for('home'))
    else:
        flash('אנא התחבר קודם!', 'danger')
        return redirect(url_for('login'))

# DISPLAY ALL REPORTS THAT THE USER CAN DOWNLOAD/DISPLAY


@ app.route("/reports", methods=["GET", "POST"])
def reports():
    try:

        if 'loggedin' in session:
            if request.method == "GET":
                log.inf_write("Page.Init completed - reports Page.")
                return render_template("reports.html", orders=Orders(db).get_orders_by_supplier(), reports_list=Reports(db).show_reports_types(), title='דוחות', logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - reports Page.")
        log.err_write("error with reports:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))

######################################################
#                      Contacts                      #
######################################################

# DISPLAY ALL CONTACTS


@ app.route("/contacts")
def contacts():
    try:
        if 'loggedin' in session:
            contacts = Contacts(db, " ", "", "", "", "", "")
            cities_list = Contacts(
                db, "", "", "", "", "", 1).get_cities()
            log.inf_write("Page.Init completed - contacts Page.")
            return render_template("contacts.html", title='אנשי קשר', contacts=contacts.get_contacts(), logged_user=session['name'],
                                   taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)), cities_list=cities_list)
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - contacts Page.")
        log.err_write("error with contacts:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))

# ADD NEW CONTACT


@ app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    try:
        form = ContactForm()
        if 'loggedin' in session:
            cities_list = Contacts(
                db, "", "", "", "", "", 1).get_cities()
            form.city.choices = [(name, name) for name in cities_list]
            if form.validate_on_submit():
                name = form.name.data
                street = form.address.data
                city = form.city.data
                phone = form.phone.data
                mail = form.mail.data
                contacts = Contacts(
                    db, name, street, city, phone, mail, 1)
                if contacts.add_contact():
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    log.inf_write("Page.Init completed - add_contact Page.")
                    log.query_write(
                        "INSERT INTO contacts(email, fullname, phone, address,city)")
                    log.inf_write("new contact add - name:" + name)
                    flash(f'!איש קשר {form.name.data} נוצר בהצלחה', 'success')
                    return redirect(url_for('contacts'))
                else:
                    flash('לא ניתן להוסיף איש קשר, איש קשר קיים במערכת', 'danger')
            return render_template('addContact.html', title='אנשי קשר', form=form, logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - add_contact Page.")
        log.err_write("error with contacts:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))


# EDIT A SPECIFIC CONTACT


@ app.route("/edit_contact", methods=['GET', 'POST'])
def edit_contact():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                id = request.args.get('id')
                name = request.args.get('name')
                street = request.args.get('street')
                city = request.args.get('city')
                phone = request.args.get('phone')
                mail = request.args.get('mail')
                contacts = Contacts(
                    db, name, street, city, phone, mail, "")
                contacts.edit_contact(str(id))
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.inf_write(
                    "contact: " + name + " edit in database.")
                return redirect(url_for('contacts'))
            return redirect(url_for('contacts'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - edit_contact Page.")
        log.err_write("error with edit_contact:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))
# CHANGE CONTACT STATUS, ACTIVE OR INACTIVE


@ app.route("/change_contact_status", methods=['GET', 'POST'])
def change_contact_status():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                if request.args:
                    id = request.args.get('id')
                    status = request.args.get('status')
                    Contacts(db, "", "", "", "", "",
                             "").change_contact_status(id, status)
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                    return redirect(url_for('contacts'))
            return redirect(url_for('contacts'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - change_contact_status Page.")
        log.err_write("error with change_contact_status:   " +
                      str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))
    ######################################################
    #                      Mail                          #
    ######################################################

# SEND AN EMAIL


@ app.route("/mail", methods=['GET', 'POST'])
def mail():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - mail Page.")
            names_list = Mail_Class(db, app, "", "", "").get_names_for_mail(
            ) + Suppliers(db).get_supplier_names()
            form = MailForm()
            app.config['MAIL_USERNAME'] = Xml().email_get()
            app.config['MAIL_PASSWORD'] = read_email_encrypted_password(Xml().pass_get())
            form.name.choices = [(name, name)
                                 for name in names_list]
            if form.validate_on_submit():
                mail_to = form.name.data
                contacts = Contacts(
                    db, mail_to, "", "", "", "", "")
                mail_address = contacts.get_contact_email()[0]
                header = form.header.data
                mail_msg = form.msg.data
                mail = Mail_Class(
                    db, app, header, mail_msg, mail_address)
                mail.send_mail()
                log.inf_write(
                    "Email to: " + mail_to + " Sent successfully")
                flash(f'מייל נשלח בהצלחה ל {mail_to}', 'success')
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.inf_write("Page.Init completed - mail Page.")
                return redirect(url_for('mail'))
            return render_template("mail.html", form=form, title='מייל', logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - mail Page.")
        log.err_write("error with mail:   " + str(error.__doc__))
        flash('שגיאה בשליחת המייל, אנא בדוק את הגדרות המייל שלך או את המייל אליו אתה שולח', 'danger')
        return redirect(url_for('mail'))

######################################################
#                      Settings                      #
######################################################


def read_email_encrypted_password(password):
    encrypt = password[::2]
    return encrypt


def encrypt_string(password):
    encrypted_pass = ""
    for ch in password:
        encrypted_pass += ch
        encrypted_pass += random.choice(string.ascii_letters + string.digits)
    return encrypted_pass


# DISPLAY THE SETTINGS OF ALSERTS, ADVERTISMENT, MAIL


@ app.route("/settings", methods=['GET', 'POST'])
def settings():
    try:
        form = FlagForm()
        if 'loggedin' in session:
            log.inf_write("Page.Init success - settings Page.")
            if form.validate_on_submit():
                flag = form.task_alert.data
                Xml().advert_set(flag)
                flag = form.advert.data
                Xml().tasks_set(flag)
                email_user = form.mail.data
                email_pass = encrypt_string(form.mailpass.data)
                read_email_encrypted_password(email_pass)
                Xml().email_set(email_user, email_pass)
                items_value = form.items_alert.data
                Xml().items_set(items_value)
                items_amount_value = form.items_amount_alert.data
                items_amount = form.items_amount.data
                Xml().items_amount_set(items_amount_value, items_amount)
                Xml().sound_set(form.sound.data)
                log.inf_write("settings saved successfully.")
                flash('הגדרות עודכנו בהצלחה!', 'success')
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                log.inf_write("Page.Init completed - settings Page.")
                return redirect(url_for('settings'))
            return render_template("settings.html", form=form, title='הגדרות', logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - settings Page.")
        log.err_write("error with settings:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))

######################################################
#                      Calculator                    #
######################################################

# DISPLAY THE CALCULATOR


@ app.route("/calc")
def calc():
    try:
        if 'loggedin' in session:
            log.inf_write("Page.Init completed - calc Page.")
            return render_template("calc.html", logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - calc Page.")
        log.err_write("error with calc:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))

######################################################
#                      Tasks                         #
######################################################

# DISPLAY ALL TASKS


@ app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    try:
        if 'loggedin' in session:
            tasks = Tasks(db, "",
                          "", "", "")
            tasks_data = tasks.get_all_tasks()
            users = Users(db, " ", " ", " ")
            names = users.get_employees_names()  # send names to.
            log.inf_write("Page.Init completed - tasks Page.")
            return render_template('tasks.html', title='משימות', value=tasks_data, names=names, logged_user=session['name'],
                                   taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - tasks Page.")
        log.err_write("error with tasks:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))

# ADD NEW TASK


@ app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    try:
        if 'loggedin' in session:
            users = Users(db, " ", " ", " ")
            names = users.get_employees_names()
            names_list = list(itertools.chain(*names))
            form = TaskForm()
            form.name.choices = [(name, name) for name in names_list]
            if form.validate_on_submit():
                name = form.name.data
                task = form.task.data
                task_date = form.task_date.data
                tasks = Tasks(db, name, task, task_date, "")
                tasks.add_task()
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)
                flash('משימה נוספה בהצלחה!', 'success')
                log.query_write(
                    "INSERT INTO tasks(employee_name, task, task_date)  VALUES(%s,%s,%s) (name, task, task_date)")
                return redirect(url_for('tasks'))
            return render_template('add_task.html', title='משימות', form=form, logged_user=session['name'], taskAlert=Xml().task_alert(db), alert_value=Xml().tasks_get(), alert_counter=len(Xml().task_alert(db)))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.inf_write("Page.Init failed - add_task Page.")
        log.err_write("error with add_task:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))

# DELETE A SPECIFIC TASK


@ app.route("/delete_task", methods=['GET', 'POST'])
def delete_task():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                if 'taskID' in request.args:
                    task_id = request.args.get('taskID')
                    tasks = Tasks(db, "", " ", " ", task_id)
                    tasks.delete_task()
                    log.query_write("DELETE FROM tasks WHERE task_id =%s")
                    log.inf_write("tasks number : " +
                                  task_id + " deleted.")
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)

                return redirect(url_for('tasks'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error with delete_task:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))
# DELETE ALL TASKS


@ app.route("/deleteAllTasks", methods=['GET', 'POST'])
def delete_all_tasks():
    try:
        if 'loggedin' in session:
            if request.method == 'GET':
                try:
                    tasks = Tasks(db, "", " ", " ", " ")
                    tasks.delete_all_tasks()
                    if Xml().sound_get():
                        winsound.PlaySound(
                            "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)

                    log.query_write("DELETE FROM tasks")
                    log.inf_write("all tasks deleted.")
                    return redirect(url_for('tasks'))
                except IndexError:
                    flash('שגיאה!', 'danger')
                    return redirect(url_for('home'))
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error with deleteAllTasks:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        return redirect(url_for('home'))
# COMPLETE TASK


@ app.route("/completeTask", methods=['GET', 'POST'])
def completeTask():
    try:
        if 'loggedin' in session:
            if 'id' in request.args:
                taskId = request.args.get('id')
                tasks = Tasks(db, "", " ", " ", taskId)
                tasks.completed_tasks()
                if Xml().sound_get():
                    winsound.PlaySound(
                        "static/sounds/WindowsDing.wav", winsound.SND_ASYNC)

                log.query_write(
                    "UPDATE tasks SET completed = TRUE WHERE task_id = " + taskId)
                log.inf_write("task : " + taskId +
                              " complete successfully.")
            if session['isAdmin'] == '1':
                ct = Tasks(db, "", "", "",
                           "").count_completed_tasks_for_dashboard()
                return render_template('home.html', taskAlert=Xml().task_alert(db),
                                       alert_value=Xml().tasks_get(), advert=Xml().advert_get(), ct=ct, logged_user=session['name'])
            else:
                return render_template('employeehome.html', taskAlert=Xml().task_alert(db),
                                       alert_value=Xml().tasks_get(), advert=Xml().advert_get(), logged_user=session['name'])
        else:
            flash('אנא התחבר קודם!', 'danger')
            return redirect(url_for('login'))
    except Exception as error:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write("error with completeTask:   " + str(error.__doc__))
        flash('שגיאה', 'danger')
        if session['isAdmin'] != '1':
            return redirect(url_for('employee_home'))
        return redirect(url_for('home'))


if __name__ == "__main__":
    try:
        app.run(debug=True)
        log.inf_write("App started successfully!")
    except Exception as e:
        if Xml().sound_get():
            winsound.PlaySound(
                "static/sounds/Windows Pop-up Blocked.wav", winsound.SND_ASYNC)
        log.err_write(str(e))
