from flask import Blueprint, render_template, request, session
import shelve
from Loan import Loan

bookings = Blueprint("bookings", __name__)

@bookings.route("/<int:id>", methods=["GET"])
def index(id):

    items_dict = {}
    db = shelve.open('items.db', 'c')

    # handle errors

    try:
        items_dict = db['Items']
    except:
        print("Error in retrieving items")

    item = items_dict[id]

    return render_template("book_item.html", item=item)

@bookings.route("/<int:id>/date", methods=["GET"])
def date(id):

    items_dict = {}
    db = shelve.open('items.db', 'c')

    # handle errors

    try:
        items_dict = db['Items']
    except:
        print("Error in retrieving items")

    item = items_dict[id]
    print(item.get_vendor_id())


    return render_template("book_item_date.html", item=item, naming=item.get_vendor_id())

@bookings.route("/create", methods=["POST"])
def create():
    cart = request.json

    items_dict = {}
    db1 = shelve.open('items.db', 'c')

    loans_dict = {}
    db2 = shelve.open('loans.db', 'c')

    # handle errors

    try:
        items_dict = db1['Items']
        loans_dict = db2['Loans']
        db1.close()
        db2.close()
    except:
        print("Error in retrieving items")

    for i in cart:
        id = int(i["id"])
        print(items_dict)
        item = items_dict[id]

        print(item.__dict__)

        identity = session['identification']
        print(identity)

        loan = Loan(item.get_item_pic(), item.get_item_name(), int(i["start"]), int(i["end"]), )

