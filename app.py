from flask import Flask, render_template, request, redirect, flash

from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


def get_db():
    return sqlite3.connect("expenses.db")



@app.route("/")
def home():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("Select * from expenses order by id desc")
    expenses = cur.fetchall()
    category = request.args.get("category")
    total = sum(i[2] for i in expenses)
    summary = {}
    monthly= {}

    if category:
        expenses = [i for i in expenses if i[3].lower() == category.lower()]

    for i in expenses:
        cat = i[3]
        summary[cat] = summary.get(cat, 0) + i[2]

        date = datetime.strptime(i[4],"%d-%m-%Y")
        month_year = date.strftime("%B %Y")
        monthly[month_year] = monthly.get(month_year,0) + i[2]

    monthly = dict(sorted(monthly.items(), reverse=True))
    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        errors={},
        form_data={},
        total=total,
        summary=summary,
        monthly = monthly
    )


@app.route("/add", methods=["POST"])
def add():

    name = request.form.get("name")
    amt = request.form.get("amt")
    category = request.form.get("category")
    date = datetime.now().strftime("%d-%m-%Y")
    errors = {}

    if not name:
        errors["name"] = "Name is required"
    if not amt:
        errors["amt"] = "Amount is required"
    else:
        try:
            amt = int(amt)
        except:
            errors["amt"] = "Amount must be in number"
    if not category:
        errors["category"] = "Category is required"        

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "Insert into expenses(Name, Amount, Category, Date) values (?,?,?,?)",
        (name, amt, category, date),
    )

    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    if not id:
        return "Invalid request"

    id = int(id)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("Delete from expenses where id = ?",(id,))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit")
def edit():
    id = int(request.args.get("id"))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("Select * from expenses where id = ?",(id,))
    exp = cur.fetchone()

    conn.close()

    if exp:
        return render_template("edit.html",exp=exp)

    return "Expense not found"


@app.route("/update", methods=["POST"])
def update():
    id = int(request.form.get("id"))
    name = request.form.get("name")
    amt = request.form.get("amt")
    category = request.form.get("category")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("Update expenses set Name = ?, Amount = ?, Category = ? where id = ?", (name,amt, category, id))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
