from flask import Blueprint, render_template, request, session
import shelve
from Loan import Loan
import time
from datetime import datetime

loansBP = Blueprint("loans", __name__)

@loansBP.route("/upcoming", methods=["GET"])
def upcoming():

    loans = []

    loans_dict = {}
    db = shelve.open('loans.db', 'c')

    
    loans_dict = db['Loans']
    db.close()

    currentTime = round(time.time())

    for id, loan in loans_dict.items():
        print(loan.__dict__)
        if loan.get_start_date()/1000 > currentTime:
            print(loan.get_start_date()/1000)
            print(currentTime)
            print(loan.get_start_date()/1000 < currentTime)
            loan.set_start_date(datetime.utcfromtimestamp(loan.get_start_date()/1000).strftime('%Y-%m-%d'))
            loan.set_end_date(datetime.utcfromtimestamp(loan.get_end_date()/1000).strftime('%Y-%m-%d'))
            loans.append(loan)

    return render_template("loans/upcoming.html", loans=loans)

@loansBP.route("/ongoing", methods=["GET"])
def ongoing():

    loans = []

    loans_dict = {}
    db = shelve.open('loans.db', 'c')

    
    loans_dict = db['Loans']
    db.close()

    currentTime = round(time.time())

    for id, loan in loans_dict.items():
        if loan.get_start_date()/1000 < currentTime and loan.get_end_date()/1000 > currentTime:
            loan.set_start_date(datetime.utcfromtimestamp(loan.get_start_date()/1000).strftime('%Y-%m-%d'))
            loan.set_end_date(datetime.utcfromtimestamp(loan.get_end_date()/1000).strftime('%Y-%m-%d'))
            loans.append(loan)

    return render_template("loans/ongoing.html", loans=loans)

@loansBP.route("/previous", methods=["GET"])
def previous():

    loans = []

    loans_dict = {}
    db = shelve.open('loans.db', 'c')

    
    loans_dict = db['Loans']
    db.close()

    currentTime = round(time.time())

    for id, loan in loans_dict.items():
        print(loan.__dict__)
        print(currentTime)
        print(loan.get_end_date()/1000 > currentTime)
        if loan.get_end_date()/1000 < currentTime:
            loan.set_start_date(datetime.utcfromtimestamp(loan.get_start_date()/1000).strftime('%Y-%m-%d'))
            loan.set_end_date(datetime.utcfromtimestamp(loan.get_end_date()/1000).strftime('%Y-%m-%d'))
            loans.append(loan)

    return render_template("loans/previous.html", loans=loans)
