from app import app, db
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from app.models import Expense

#This route renders the homepage which contains a form to recieve expense data from user
@app.route("/")
def home():
    return render_template("add.html")

#This route collects the data from the user and creates an object with it when submitted
#This route also triggers the "/expenses" route using the redirect function
@app.route("/addexpense",methods=["POST"])
def addexpense():
    # extracting the data from the form using the request object from flask
    date = request.form["date"]
    expensename = request.form["expensename"]
    amount = request.form["amount"]
    category = request.form["category"]
    #print values to check if values of the form fields are actualy being extracted
    print(date + " " + expensename + " " + amount + " " + category)
    #Creating an expense object
    expense = Expense(
        date=date,
        expensename=expensename,
        amount=amount,
        category=category
        )
    #Adding the object to the database
    db.session.add(expense)
    db.session.commit()
    return redirect("/expenses")

# This route retrieves all items in the database and renders it in the expenses.html template
# This route also calculates the total expenses on each category and sends it to the template
@app.route("/expenses")
def expenses():
    expenses = Expense.query.all()
    total = 0
    t_food = 0
    t_business = 0
    t_enter = 0
    t_trans = 0
    t_other = 0
    for item in expenses:
        total += item.amount
        if item.category == "business":
            t_business +=item.amount
        elif item.category == "food":
            t_food +=item.amount
        elif item.category == "entertainment":
            t_enter +=item.amount
        elif item.category == "transport":
            t_trans +=item.amount
        elif item.category == "other":
            t_other +=item.amount
    # Sending values to expenses.html template
    return render_template(
        "expenses.html",
        expenses=expenses,
        total=total,
        t_business=t_business,
        t_food=t_food,
        t_enter=t_enter,
        t_trans=t_trans,
        t_other=t_other
        )

# This route defines the delete functionality button

@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect("/expenses")


# This route retrieves the expense whose edit button has been clicked
# The retrieved object is rendered on updateexpense.html template
# The updateexpense.html template is simply a form for editing the expenses
# Infact updateexpense form is exactly the same as that of the add.html template 
@app.route("/update/<int:id>")
def update(id):
    """ Retrieves the expense whose edit button was clicked """
    expense = Expense.query.filter_by(id=id).first()
    return render_template("updateexpense.html", expense=expense)


@app.route("/edit", methods=["POST"])
def edit():
    """requesting data from the form fields with the syntax:
    request.form["field_name"] """
    id = request.form["id"]
    date = request.form["date"]
    expensename = request.form["expensename"]
    amount = request.form["amount"]
    category = request.form["category"]

    expense = Expense.query.filter_by(id=id).first()
# So now instead of creating a new object, I will just set the values of current object
# which we just querried from the database to the new values received from the form.
    expense.date = date
    expense.expensename = expensename
    expense.amount = amount
    expense.category = category

    # Next commit the changes to the database
    db.session.commit()
    return redirect("/expenses")


@app.route("/addview",methods=["GET","POST"])
def addview():
    if request.method == "GET":
        expenses = Expense.query.all()
        total = 0
        t_food = 0
        t_business = 0
        t_enter = 0
        t_trans = 0
        t_other = 0
        for item in expenses:
            total += item.amount
            if item.category == "business":
                t_business +=item.amount
            elif item.category == "food":
                t_food +=item.amount
            elif item.category == "entertainment":
                t_enter +=item.amount
            elif item.category == "transport":
                t_trans +=item.amount
            elif item.category == "other":
                t_other +=item.amount

    elif request.method=="POST":
         # extracting the data from the form using the request object from flask
        date = request.form["date"]
        expensename = request.form["expensename"]
        amount = request.form["amount"]
        category = request.form["category"]
    #print values to check if values of the form fields are actualy being extracted
        print(date + " " + expensename + " " + amount + " " + category)
    #Creating an expense object
        expense = Expense(
            date=date,
            expensename=expensename,
            amount=amount,
            category=category
        )
    #Adding the object to the database
        db.session.add(expense)
        db.session.commit()
        return redirect("/addview")

    # Sending values to addview.html template
    return render_template(
        "addview.html",
        expenses=expenses,
        total=total,
        t_business=t_business,
        t_food=t_food,
        t_enter=t_enter,
        t_trans=t_trans,
        t_other=t_other
        )