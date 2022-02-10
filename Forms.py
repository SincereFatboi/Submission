from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, RadioField, SelectField, EmailField, TextAreaField, DateField, PasswordField, IntegerField, FileField, DecimalField, validators, ValidationError
#from wtforms.fields.html5 import EmailField
from wtforms.widgets import PasswordInput


class CreateUserForm(Form):
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired(), validators.EqualTo('password_confirm')])
    password_confirm = PasswordField('Confirm Password', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateCustomerForm(Form):
    def repeat_username(form, field):
        with open('customerDatabase.txt', 'r') as file:
            for line in file:
                different = line.split('<,./;>')
                if str(field.data) == str(different[1]):
                    raise ValidationError('This username is already taken!')
    username = StringField('Username', [validators.Length(min=1, max=100), validators.DataRequired()])
    def repeat_email(form, field):
        with open('customerDatabase.txt', 'r') as file:
            for line in file:
                different = line.split('<,./;>')
                if str(field.data) == str(different[2]):
                    raise ValidationError('This email is already taken!')
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Confirm Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    password_confirm = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired(), validators.EqualTo('password_confirm', message="Passwords must match!")])


class UpdateCustomerForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=100), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = StringField('Password', widget=PasswordInput(hide_value=False))


class CustomerSignIn(Form):
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password')


class CreateVendorForm(Form):
    def repeat_username(form, field):
        with open('vendorDatabase.txt', 'r') as file:
            for line in file:
                different = line.split('<,./;>')
                if str(field.data) == str(different[2]):
                    raise ValidationError('This username is already taken')
    username = StringField('Username', [validators.Length(min=1, max=100), validators.DataRequired(), repeat_username])
    name = StringField('Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    def repeat_email(form, field):
        with open('vendorDatabase.txt', 'r') as file:
            for line in file:
                different = line.split('<,./;>')
                if str(field.data) == str(different[4]):
                    raise ValidationError('This email is already taken!')
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), repeat_email])
    mobile = StringField('Mobile Number', [validators.Length(min=1, max=8), validators.DataRequired()])
    password = PasswordField('Confirm Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    password_confirm = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired(), validators.EqualTo('password_confirm', message="Passwords must match!")])


class UpdateVendorForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=100), validators.DataRequired()])
    name = StringField('Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    mobile = StringField('Mobile Number', [validators.Length(min=1, max=8), validators.DataRequired()])
    password = StringField('Password', widget=PasswordInput(hide_value=False))

class VendorSignIn(Form):
    username = StringField('Username', [validators.Length(min=1, max=100), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password')


class CreateItemForm(Form):
    image = FileField(u'Image File')
    name = StringField('Item Name', [validators.Length(min = 1, max = 150), validators.DataRequired()], render_kw={"placeholder": "Enter Item name"})
    description = TextAreaField('Description', [validators.DataRequired()] ,render_kw={"rows": 10, "cols": 11})
    rate = DecimalField('Daily Rate', [validators.number_range(min=0),validators.InputRequired()])
    on_loan = IntegerField('On Loan', [validators.number_range(min=0),validators.InputRequired()])
    available = IntegerField('Inventory stock', [validators.number_range(min=1),validators.InputRequired()])
    location = StringField('Pickup/Dropoff location', [validators.Length(min = 1, max = 1000), validators.DataRequired()])


class CreateLoanForm(Form):
    item_pic = FileField(u'Image File')
    item_name = StringField('Item Name', [validators.Length(min = 1, max = 150), validators.DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    customer_name = StringField('Customer Name', [validators.Length(min = 1, max = 150), validators.DataRequired()])





    # def __init__(self, *args, **kwargs):
    #     super(CustomerSignIn, self).__init__(*args, **kwargs)
    #
    # def sign_in_authentication(self):
    #     initial_validation = super(CustomerSignIn, self).validate()
    #     if not initial_validation:
    #         return False
    #     with open('customerDatabase.txt', 'r') as file:
    #         for line in file:
    #             different = line.split('<,./;>')
    #             if str(self.username) != str(different[1]) or str(self.data) != str(different[2] or str(self.password) != different[3]):
    #                 print('It works')
    #                 raise ValidationError('Wrong!')








