from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateUserForm, CreateCustomerForm, UpdateCustomerForm, CustomerSignIn, CreateVendorForm, UpdateVendorForm
from Customer import Customer
from Vendor import Vendor
import os
import sys
import subprocess
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, EmailField, DateField, PasswordField, \
    validators, ValidationError

app = Flask(__name__)


@app.route('/')
def home():
    app.secret_key = 'random123random098'
    return render_template('home.html')


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
            return redirect(url_for('retrieve_customers'))
    return render_template('updateCustomer.html', update_customer_form=update_customer_form,
                           prefill_customer_form=prefill_customer_form)


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


# @app.route('/customerSignIn', methods=['GET', 'POST'])
# def customer_sign_in():
#     customer_sign_in = CustomerSignIn(request.form)
#     if request.method == 'POST' and customer_sign_in.validate():
#         with open('customerDatabase.txt', 'r') as file:
#             for line in file:
#                 different = line.split('<,./;>')
#                 print(different)
#                 print(customer_sign_in.email.data)
#                 print(customer_sign_in.password.data)
#                 if str(customer_sign_in.email.data) == str(
#                         different[2]) and str(customer_sign_in.password.data) == str(different[3]):
#                     print('Yes, you are signed in!')
#                     identity = different[0]
#                     print(identity)
#
#                     return redirect(url_for('customer_account_page', id=identity))
#         if str(customer_sign_in.email.data) != str(
#                 different[2]) or str(customer_sign_in.password.data) != str(different[3]):
#             print('No, you are not signed in!')
#             customer_sign_in.password.errors = ['Either your password or email is wrong']
#             customer_sign_in.email.data = ''
#     return render_template('customerSignIn.html', customer_sign_in=customer_sign_in)


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


@app.route('/createVendor', methods=['GET', 'POST'])
def create_vendor():
    create_vendor_form = CreateVendorForm(request.form)
    if request.method == 'POST' and create_vendor_form.validate():
        vendor_id = Vendor(create_vendor_form.name.data, create_vendor_form.username.data,
                           create_vendor_form.email.data, create_vendor_form.mobile.data,
                           create_vendor_form.password.data, create_vendor_form.password_confirm.data).get_vendor_id()
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
            return redirect(url_for('retrieve_vendors'))
    return render_template('updateVendor.html', update_vendor_form=update_vendor_form,
                           prefill_vendor_form=prefill_vendor_form)


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
        return redirect(url_for('customer_account_page', id=identity))
    if request.method == 'POST' and customer_sign_in.validate():
        with open('customerDatabase.txt', 'r') as file, open('vendorDatabase.txt', 'r') as file2:
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
                    return redirect(url_for('vendor_account_page', id=identity))
        if str(customer_sign_in.email.data) != str(different[2]) or str(customer_sign_in.password.data) != str(different[3]):
            customer_sign_in.password.errors = ['Either your password or email is wrong']
            customer_sign_in.email.data = ''
    return render_template('customerSignIn.html', customer_sign_in=customer_sign_in)


@app.route('/vendorAccountPage/<id>')
def vendor_account_page(id):
    print('Hello')
    with open('vendorDatabase.txt', 'r') as file:
        for lines in file:
            look = lines.split('<,./;>')
            if str(id) == str(look[0]):
                break
    return render_template('vendorAccountPage.html', look=look)
#cool
if __name__ == '__main__':
    app.run(port=8000)
