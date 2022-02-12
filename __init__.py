from flask import Flask, render_template, request, redirect, url_for, session

from Chat import Chat, Message
from Forms import CreateUserForm, CreateCustomerForm, UpdateCustomerForm, CustomerSignIn, CreateVendorForm, UpdateVendorForm, CreateItemForm, CreateLoanForm
from Customer import Customer
from Vendor import Vendor
import os
import sys
import random
import subprocess
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, DateField, PasswordField, \
    validators, ValidationError
import shelve
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for
import Item
import Loan
from routes.booking import bookings

app = Flask(__name__)
app.register_blueprint(bookings, url_prefix="/book")

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/payment')
def payment():
    return render_template("payments.html")

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/')
def home():
    app.secret_key = 'random123random098'
    if 'identification' not in session:
        return redirect(url_for('customer_store'))
    else:
        account = session['identification']

        total_items_dict = {}
        db = shelve.open('items.db', 'c')

        try:
            total_items_dict = db['Items']

        except IndexError:
            print("Error in retrieving items")

        db.close()

        items_list = []

        for key in total_items_dict:
            item = total_items_dict.get(key)
            items_list.append(item)

        random.shuffle(items_list)



    return render_template('home.html', items_list=items_list, account=account)

@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customer_id = Customer(create_customer_form.username.data, create_customer_form.email.data,
                               create_customer_form.password.data,
                               create_customer_form.password_confirm.data).get_customer_id()
        with open('customerDatabase.txt', 'a') as file:
            file.write(
                str(customer_id) + '<,./;>' + create_customer_form.username.data + '<,./;>' + create_customer_form.email.data + '<,./;>' + create_customer_form.password.data + '<,./;>' + '\n')
        return redirect(url_for('home'))
    return render_template('createCustomer.html', form=create_customer_form)
#sup

@app.route('/retrieveCustomers')
def retrieve_customers():
    customer_list = []
    with open('customerDatabase.txt', 'r') as file:
        for line in file:
            splitlist = line.split('<,./;>')
            customer_list.append(splitlist)
    return render_template('retrieveCustomers.html', count=len(customer_list), splitlist=splitlist,
                           customer_list=customer_list)


@app.route('/updateCustomer/<string:unique>', methods=['GET', 'POST'])
def update_customer(unique):
    prefill_customer_form = UpdateCustomerForm(request.form)
    update_customer_form = UpdateCustomerForm(request.form)
    try:
        with open('customerDatabase.txt', 'r') as file:
            all_lines = file.readlines()
            for i, j in enumerate(all_lines):
                if unique in j:
                    specific_line = all_lines[i]
                    specific_line = specific_line.split('<,./;>')
                    break
            print(specific_line)
            idk = specific_line[0]
            prefill_customer_form.username.data = specific_line[1]
            prefill_customer_form.email.data = specific_line[2]
            prefill_customer_form.password.data = specific_line[3]
    except Exception as e:
        print(e)
    else:
        if request.method == 'POST' and update_customer_form.validate():
            all_lines[i] = str(specific_line[0]) + '<,./;>' + update_customer_form.username.data + '<,./;>' + update_customer_form.email.data + '<,./;>' + update_customer_form.password.data + '<,./;>' + '\n'
            with open('customerDatabase.txt', 'w') as file:
                file.writelines(all_lines)
            zoom = session['identification']
            if zoom[:1] == 'A':
                return redirect(url_for('retrieve_customers'))
            elif zoom[:1] == 'C':
                return redirect(url_for('customer_account_page', id=zoom))
    return render_template('updateCustomer.html', update_customer_form=update_customer_form,
                           prefill_customer_form=prefill_customer_form, idk=idk)

@app.route('/updateAdmin', methods=['GET', 'POST'])
def update_admin():
    prefill_customer_form = UpdateCustomerForm(request.form)
    update_customer_form = UpdateCustomerForm(request.form)
    with open('adminDetails.txt', 'r') as file:
        for line in file:
            specific_line = line.split('<,./;>')


            prefill_customer_form.username.data = specific_line[2]
            prefill_customer_form.email.data = specific_line[0]
            prefill_customer_form.password.data = specific_line[1]
    if request.method == 'POST' and update_customer_form.validate():
        all_lines = update_customer_form.email.data + '<,./;>' + update_customer_form.password.data + '<,./;>' + update_customer_form.username.data + '<,./;>' + 'A31c1c332-ab52-48c5-a64b-7c1b9d978d52' + '\n'
        with open('adminDetails.txt', 'w') as file:
            file.writelines(all_lines)
        return redirect(url_for('admin_account_page'))

    return render_template('updateAdmin.html', update_customer_form=update_customer_form, prefill_customer_form=prefill_customer_form)



@app.route('/deleteCustomer/<string:unique>', methods=['GET', 'POST'])
def delete_customer(unique):
    if request.method == 'POST':
        try:
            with open("customerDatabase.txt", "r") as file:
                read_all = file.readlines()
            with open("customerDatabase.txt", "w") as file:
                for i in range(len(read_all)):
                    no_delete = read_all[i]
                    no_delete_list = no_delete.split('<,./;>')
                    if str(no_delete_list[0]) != unique:
                        file.write(no_delete)
        except Exception as e:
            print(e)
        else:
            return redirect(url_for('retrieve_customers'))
    return render_template('updateCustomer.html')


@app.route('/customerAccountPage/<id>')
def customer_account_page(id):
    with open('customerDatabase.txt', 'r+') as file:
        for line in file:
            by_line = line.split('<,./;>')
            if by_line[0] == id:
                with open('idNumber.txt', 'w') as second_file:
                    print(line)
                    second_file.write(line)
                    break
    with open('customerDatabase.txt', 'r') as file:
        many_lines = file.readlines()
        for i, j in enumerate(many_lines):
            if id in j:
                one_line = many_lines[i]
                one_line = one_line.split('<,./;>')
    return render_template('customerAccountPage.html', one_line=one_line)

@app.route('/adminAccountPage')
def admin_account_page():
    with open('adminDetails.txt', 'r+') as file:
        for line in file:
            print('Shitty Loop')
            pro = line.split('<,./;>')
            break
        print(pro)
    return render_template('adminAccountPage.html', pro=pro)


@app.route('/createVendor', methods=['GET', 'POST'])
def create_vendor():
    create_vendor_form = CreateVendorForm(request.form)
    if request.method == 'POST' and create_vendor_form.validate():
        vendor_id = Vendor(create_vendor_form.name.data, create_vendor_form.username.data,
                           create_vendor_form.email.data, create_vendor_form.mobile.data,
                           create_vendor_form.password.data, create_vendor_form.password_confirm.data).get_vendor_id()

        items_dict = {}
        delete_dict = {}

        db = shelve.open(str(vendor_id) + '.db', 'c')


        items_dict[vendor_id] = 4

        db['vendorItems'] = items_dict

        delete_dict = db['vendorItems']

        delete_dict.clear()

        db['vendorItems'] = delete_dict



        db.close()

        with open('vendorDatabase.txt', 'a') as file:
            file.write(str(vendor_id) + '<,./;>' + str(create_vendor_form.name.data) + '<,./;>' + str(create_vendor_form.username.data) + '<,./;>' + str(create_vendor_form.mobile.data) + '<,./;>' + str(create_vendor_form.email.data) + '<,./;>' + str(create_vendor_form.password.data) + '<,./;>' + '\n')
        return redirect(url_for('home'))
    return render_template('createVendor.html', create_vendor_form=create_vendor_form)


@app.route('/retrieveVendors')
def retrieve_vendors():
    vendor_list = []
    with open('vendorDatabase.txt', 'r') as file:
        for line in file:
            splitlist = line.split('<,./;>')
            vendor_list.append(splitlist)
    return render_template('retrieveVendors.html', count=len(vendor_list), splitlist=splitlist,
                           vendor_list=vendor_list)


@app.route('/updateVendor/<string:unique>', methods=['GET', 'POST'])
def update_vendor(unique):
    prefill_vendor_form = UpdateVendorForm(request.form)
    update_vendor_form = UpdateVendorForm(request.form)
    try:
        with open('vendorDatabase.txt', 'r') as file:
            all_lines = file.readlines()
            for i, j in enumerate(all_lines):
                if unique in j:
                    specific_line = all_lines[i]
                    specific_line = specific_line.split('<,./;>')
                    break
            print(specific_line)
            idk = specific_line[0]
            prefill_vendor_form.name.data = specific_line[1]
            prefill_vendor_form.username.data = specific_line[2]
            prefill_vendor_form.mobile.data = specific_line[3]
            prefill_vendor_form.email.data = specific_line[4]
            prefill_vendor_form.password.data = specific_line[5]
    except Exception as e:
        print(e)
    else:
        if request.method == 'POST' and update_vendor_form.validate():
            all_lines[i] = str(specific_line[0]) + '<,./;>' + update_vendor_form.name.data + '<,./;>' + update_vendor_form.username.data + '<,./;>' + update_vendor_form.mobile.data + '<,./;>' + update_vendor_form.email.data + '<,./;>' + update_vendor_form.password.data + '<,./;>' + '\n'
            with open('vendorDatabase.txt', 'w') as file:
                file.writelines(all_lines)
            zoom = session['identification']
            if zoom[:1] == 'A':
                return redirect(url_for('retrieve_vendors'))
            elif zoom[:1] == 'V':
                return redirect(url_for('vendor_account_page', id=zoom))
    return render_template('updateVendor.html', update_vendor_form=update_vendor_form,
                           prefill_vendor_form=prefill_vendor_form, idk=idk)


@app.route('/deleteVendor/<string:unique>', methods=['GET', 'POST'])
def delete_vendor(unique):
    if request.method == 'POST':
        try:
            with open("vendorDatabase.txt", "r") as file:
                read_all = file.readlines()
            with open("vendorDatabase.txt", "w") as file:
                for i in range(len(read_all)):
                    no_delete = read_all[i]
                    no_delete_list = no_delete.split('<,./;>')
                    if str(no_delete_list[0]) != unique:
                        file.write(no_delete)
        except Exception as e:
            print(e)
        else:
            return redirect(url_for('retrieve_vendors'))
    return render_template('updateVendors.html')

@app.route('/customerSignIn', methods=['GET', 'POST'])
def customer_sign_in():
    customer_sign_in = CustomerSignIn(request.form)
    if 'identification' in session:
        identity = session['identification']
        if identity[:1] == 'V':
            return redirect(url_for('vendor_account_page', id=identity))
        elif identity[:1] == 'C':
            return redirect(url_for('customer_account_page', id=identity))
        elif identity[:1] == 'A':
            return redirect(url_for('admin_account_page'))
    if request.method == 'POST' and customer_sign_in.validate():
        with open('customerDatabase.txt', 'r') as file, open('vendorDatabase.txt', 'r') as file2, open('adminDetails.txt', 'r') as file3:
            for line in file:
                different = line.split('<,./;>')
                if str(customer_sign_in.email.data) == str(
                        different[2]) and str(customer_sign_in.password.data) == str(different[3]):
                    print('You are customer!')
                    identity = different[0]
                    session['identification'] = identity
                    return redirect(url_for('customer_account_page', id=identity))
            for line2 in file2:
                different2 = line2.split('<,./;>')
                print(different2[4])
                if str(customer_sign_in.email.data) == str(different2[4]) and str(customer_sign_in.password.data) == str(different2[5]):
                    identity = different2[0]
                    session['identification'] = identity
                    return redirect(url_for('vendor_account_page', id=identity))
            for line3 in file3:
                different3 = line3.split('<,./;>')
                if str(customer_sign_in.email.data) == str(different3[0]) and str(customer_sign_in.password.data) == str(different3[1]):
                    identity = different3[3]
                    session['identification'] = identity
                    return redirect(url_for('admin_account_page'))
        if str(customer_sign_in.email.data) != str(different[2]) or str(customer_sign_in.password.data) != str(different[3]):
            customer_sign_in.password.errors = ['Either your password or email is wrong']
            customer_sign_in.email.data = ''
    return render_template('customerSignIn.html', customer_sign_in=customer_sign_in)


@app.route('/customerStore', methods=['GET', 'POST'])
def customer_store():
    if 'identification' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('customer_sign_in'))


@app.route('/vendorAccountPage/<id>', methods=['GET', 'POST'])
def vendor_account_page(id):
    with open('vendorDatabase.txt', 'r') as file:
        for lines in file:
            look = lines.split('<,./;>')
            if str(id) == str(look[0]):
                break
    if request.method == "POST":
        session.pop('identification', None)
        return redirect(url_for('customerSignIn'))
    return render_template('vendorAccountPage.html', look=look)

@app.route('/signOut', methods=['GET', 'POST'])
def sign_out():
    if request.method == 'POST':
        session.pop('identification', None)
        return redirect(url_for('customer_sign_in'))
    return render_template('vendorAccountPage.html')

@app.route('/emptylistingpage')
def empty_listing_page():
    return render_template('emptylistingpage.html')



@app.route('/vendorSpecificPage/<vendorid>')
def vendor_specific_page(vendorid):
    try:

        db = shelve.open(str(vendorid) + '.db', 'c')
        print(db['vendorItems'])

    except Exception as e:
        print(e, 'hello')
        return redirect(url_for('empty_listing_page'))
    else:
        items_dict = db['vendorItems']
        print(items_dict)
        db.close()
        items_list = []
        for key in items_dict:
            item = items_dict.get(key)
            items_list.append(item)



    return render_template('vendorSpecificPage.html', items_list=items_list, vendorid=vendorid)


@app.route('/listingpage/<vendorid>')
def listingpage(vendorid):
    # retrieve items from database
    print(id)


    try:

        db = shelve.open(str(vendorid) + '.db', 'c')
        print(db['vendorItems'])

    except Exception as e:
        print(e)
        return redirect(url_for('home'))
    else:
        items_dict = db['vendorItems']
        print(items_dict)
        db.close()
        items_list = []
        for key in items_dict:
            item = items_dict.get(key)
            items_list.append(item)

    return render_template('listingpage.html', items_list=items_list, vendorid=vendorid)


@app.route('/customerlistingpage/<id>')
def customerlistingpage():
    # retrieve items from database

    total_items_dict = {}
    db = shelve.open('items.db', 'c')

    try:
        total_items_dict = db['Items']

    except IndexError:
        print("Error in retrieving items")

    db.close()

    items_list = []
    for key in total_items_dict:
        item = total_items_dict.get(key)
        items_list.append(item)

    return render_template('customerlistingpage.html', items_list=items_list)

@app.route('/updateitem/<vendorid>/<int:id>/', methods=["GET", "POST"])
def update_item(vendorid, id):
    # request form to update item

    update_item_form = CreateItemForm(request.form)
    if request.method == 'POST' and update_item_form.validate():
        total_items_dict = {}
        items_dict = {}

        #open vendor database
        db = shelve.open(str(vendorid) + '.db', 'w')
        items_dict = db["vendorItems"]

        #open customer database
        db_main = shelve.open('items.db', 'w')
        total_items_dict = db_main['Items']

        item = items_dict.get(id)
        item.set_image(update_item_form.image.data)
        # request.files['image'].save(
        #     os.path.join('static/images', f"{item.get_id()}.png")
        # )
        item.set_name(update_item_form.name.data)
        item.set_description(update_item_form.description.data)
        item.set_rate(update_item_form.rate.data)
        item.set_on_loan(update_item_form.on_loan.data)
        item.set_available(update_item_form.available.data)
        item.set_location(update_item_form.location.data)
        item = total_items_dict.get(id)

        item.set_image(update_item_form.image.data)
        # request.files['image'].save(
        #     os.path.join('static/images', f"{item.get_id()}.png")
        # )
        item.set_name(update_item_form.name.data)
        item.set_description(update_item_form.description.data)
        item.set_rate(update_item_form.rate.data)
        item.set_on_loan(update_item_form.on_loan.data)
        item.set_available(update_item_form.available.data)
        item.set_location(update_item_form.location.data)
        imageName = str(id)
        request.files['image'].save(os.path.join('static/images', f"{imageName}1.png"))
        img = os.stat(os.path.join('static/images', f"{imageName}1.png")).st_size
        if img == 0:
            os.remove(os.path.join('static/images', f"{imageName}1.png"))
        else:
            im = Image.open(request.files['image'])
            im = im.save(os.path.join('static/images', f"{imageName}.png"))
            os.remove(os.path.join('static/images', f"{imageName}1.png"))

        db_main['Items'] = total_items_dict
        db_main.close()

        db['vendorItems'] = items_dict
        db.close()

        return redirect(url_for('listingpage', vendorid=vendorid))

    # display current information
    else:
        total_items_dict = {}
        items_dict = {}


        # items_list = []
        db = shelve.open('items.db', 'r')
        items_dict = db['Items']
        print(items_dict)
        item = items_dict.get(id)
        update_item_form.image.data = item.get_image()
        update_item_form.name.data = item.get_name()
        update_item_form.description.data = item.get_description()
        update_item_form.rate.data = item.get_rate()
        update_item_form.on_loan.data = item.get_on_loan()
        update_item_form.available.data = item.get_available()
        update_item_form.location.data = item.get_location()

    return render_template('updateitem.html', form=update_item_form)


# delete item
@app.route('/deleteitem/<vendorid>/<int:id>/', methods=['POST'])
def delete_item(vendorid, id):
    # retrieve item from database

    #vendor side
    total_items_dict = {}

    #customer side
    items_dict = {}

    #vendor side
    db = shelve.open(str(vendorid) + '.db', 'w')

    #customer side
    db_main = shelve.open('items.db', 'w')

    #vendor side exception handling
    try:
        items_dict = db['vendorItems']
    except IndexError:
        print("Error in retrieving items")
    #customer side vendor validation
    try:
        total_items_dict = db_main['Items']

    except IndexError:
        print("Error in retreiving items")

    # delete image from static
    os.remove(f'static/images/{id}.png')

    # delete selected item from vendor side
    items_dict.pop(id)
    # delete selected item from customer side
    total_items_dict.pop(id)

    #update vendor database
    db['vendorItems'] = items_dict
    db.close()
    # update customer database
    db_main['Items'] = total_items_dict
    db_main.close()

    return redirect(url_for('listingpage', vendorid=vendorid))


# create new itemg


@app.route('/createitem/<vendorid>', methods=['GET', 'POST'])
def create_item(vendorid):
    print(id)
    # request for item creation form

    create_item_form = CreateItemForm(request.form)

    if request.method == 'POST' and create_item_form.validate():
        total_items_dict = {}
        items_dict = {}

        #open vendor database
        db = shelve.open( str(vendorid) + '.db', 'c')

        #open customer database
        db_main = shelve.open('items.db', 'c')

        # handle errors
        try:
            total_items_dict = db_main["Items"]

        except:
            print("Error in retrieving items")


        try:
            items_dict = db['vendorItems']
        except:
            print("Error in retrieving items")

        # get information entered into form
        with open('vendorDatabase.txt', 'r') as file:
            for line in file:
                splitlist = line.split('<,./;>')
                if str(vendorid) == str(splitlist[0]):
                    username = splitlist[2]
                    print(username)

        item = Item.Item(create_item_form.image.data,
                         vendorid, username,
                         create_item_form.name.data,
                         create_item_form.description.data,
                         create_item_form.rate.data,
                         create_item_form.on_loan.data,
                         create_item_form.available.data,
                         create_item_form.location.data)
        # update customer database
        total_items_dict[item.get_id()] = item
        db_main['Items'] = total_items_dict
        db_main.close()



        #update vendor database
        items_dict[item.get_id()] = item
        db['vendorItems'] = items_dict
        db.close()

        # save image to static
        request.files['image'].save(
            os.path.join('static/images', f"{item.get_id()}.png")
        )

        return redirect(url_for('listingpage', vendorid=vendorid, username=username))
    return render_template('createItem.html', form=create_item_form, vendorid=vendorid)

@app.route('/createloan', methods=['GET', 'POST'])
def create_loan():
    create_loan_form = CreateLoanForm(request.form)
    if request.method == 'POST' and create_loan_form.validate():
        previous_loans_dict = {}
        db = shelve.open('previousloans.db', 'c')

        # handle errors

        try:
            future_loans_dict = db['PreviousLoans']
        except IndexError:
            print("Error in retrieving items")

        # get information entered into form

        loan = Loan.Loan(create_loan_form.item_pic.data,
                         create_loan_form.item_name.data,
                         create_loan_form.start_date.data,
                         create_loan_form.end_date.data,
                         create_loan_form.customer_name.data)
        # update database

        previous_loans_dict[loan.get_id()] = loan
        db['PreviousLoans'] = previous_loans_dict

        db.close()

        return redirect(url_for('listingpage'))
    return render_template('createloan.html', form=create_loan_form)


@app.route('/futureloans')
def future_loans():
    # retrieve future loans
    future_loans_dict = {}
    db = shelve.open('futureloans.db', 'r')
    future_loans_dict = db['FutureLoans']
    db.close()

    future_loans_list = []
    for key in future_loans_dict:
        loan = future_loans_dict.get(key)
        future_loans_list.append(loan)

    return render_template('futureloans.html', future_loans_list=future_loans_list)


@app.route('/currentloans')
def current_loans():
    # retrieve future loans
    current_loans_dict = {}
    db = shelve.open('currentloans.db', 'r')
    current_loans_dict = db['CurrentLoans']
    db.close()

    current_loans_list = []
    for key in current_loans_dict:
        loan = current_loans_dict.get(key)
        current_loans_list.append(loan)

    return render_template('currentloans.html', current_loans_list=current_loans_list)


@app.route('/previousloans')
def previous_loans():
    # retrieve previous loans
    previous_loans_dict = {}
    db = shelve.open('previousloans.db', 'r')
    try:
        previous_loans_dict = db['PreviousLoans']
    except:
        print("Error in retrieving items")
    db.close()

    previous_loans_list = []
    for key in previous_loans_dict:
        loan = previous_loans_dict.get(key)
        previous_loans_list.append(loan)

    return render_template('pastloans.html', previous_loans_list=previous_loans_list)


@app.route('/movetocurrent/<int:id>', methods=['POST'])
def move_to_current(id):
    future_loans_dict = {}
    current_loans_dict = {}

    # retrieve items from future loans database

    db = shelve.open('futureloans.db', 'c')
    future_loans_dict = db['FutureLoans']

    # retrieve items from current loans database

    db_current = shelve.open('currentloans.db', 'c')
    current_loans_dict = db_current['CurrentLoans']

    loan = future_loans_dict[id]
    current_loans_dict[id] = loan

    # save to current loans database
    db_current['CurrentLoans'] = current_loans_dict

    # delete item from future loans dictionary
    future_loans_dict.pop(id)
    db['FutureLoans'] = future_loans_dict

    # close database
    db.close()
    db_current.close()

    return render_template('futureloans.html')


@app.route('/movetoprev/<int:id>', methods=['POST'])
def move_to_prev(id):
    current_loans_dict = {}
    previous_loans_dict = {}


    # retrieve items from current loans database

    db = shelve.open('currentloans.db', 'c')
    current_loans_dict = db['CurrentLoans']

    # retrieve items from previous loans database

    db_prev = shelve.open('previousloans.db', 'c')
    previous_loans_dict = db_prev['PreviousLoans']

    loan = current_loans_dict[id]
    previous_loans_dict[id] = loan

    # save to previous loans database
    db_prev['PreviousLoans'] = previous_loans_dict

    # delete item from current loans dictionary
    current_loans_dict.pop(id)
    db['CurrentLoans'] = current_loans_dict

    # close database
    db.close()
    db_prev.close()

    return render_template('futureloans.html')


@app.route("/<string:TYPE>/chats/<string:ID>", methods=["GET"])
def chats(TYPE: str, ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    _chats: set[str] = Chat().getChatsByID(ID)
    __chats: list = []
    for chat_ in _chats:
        c: Chat = Chat(chat_ if TYPE else ID, ID if TYPE else chat_)
        __chats.append((chat_, c.getLastMessageObject(), c.getUnreadMessagesCount(asVendor=TYPE)))
    return render_template("chats.html", count=len(__chats), chats_list=__chats, asVendor=TYPE, me=ID)


# This is for chat, message, review, and feedback features:

@app.route("/<string:TYPE>/chats/<string:MY_ID>/<string:YOUR_ID>", methods=["GET", "POST"])
def chat(TYPE: str, MY_ID: str, YOUR_ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    CHAT: Chat = Chat(YOUR_ID if TYPE else MY_ID, MY_ID if TYPE else YOUR_ID)
    if request.method == "POST":
        CHAT.appendChatMessage(TYPE, request.form.get("text", '', str))
    c: list[Message] = CHAT.getChat()
    for i in range(len(c)):
        c[i].index = i
    c.reverse()
    with open('vendorDatabase.txt', 'r') as file:
        for line in file:
            splitlist = line.split('<,./;>')
            if str(YOUR_ID) == str(splitlist[0]):
                username = splitlist[1]
    return render_template("chat.html", asVendor=TYPE, me=MY_ID, you=YOUR_ID, chat=c, username=username)


# This is for chat, message, review, and feedback features:

@app.route("/<string:TYPE>/chats/<string:MY_ID>/<string:YOUR_ID>/edit", methods=["POST"])
def edit_chat(TYPE: str, MY_ID: str, YOUR_ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    CHAT: Chat = Chat(YOUR_ID if TYPE else MY_ID, MY_ID if TYPE else YOUR_ID)
    try:
        index: int = int(request.json.get('i', -1))
        newMsg: str = str(request.json.get("msg", ''))
        if MY_ID == CHAT.getChat()[index].id() and CHAT.editChatMessage(index, newMsg):
            return '', 200
    except:
        pass
    return '', 403


# This is for chat, message, review, and feedback features:

@app.route("/<string:TYPE>/deleteChat/<string:MY_ID>/<string:YOUR_ID>", methods=["POST"])
def delete_chat(TYPE: str, MY_ID: str, YOUR_ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    if Chat(YOUR_ID if TYPE else MY_ID, MY_ID if TYPE else YOUR_ID).delChat():
        return redirect(url_for("chats", TYPE=("vendor" if TYPE else "customer"), ID=MY_ID))



if __name__ == '__main__':
    app.run(port=8000, debug=True)
