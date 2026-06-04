from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

CSV_FILE = "tasks.csv"


# ---------------------------
# READ TASKS
# ---------------------------
def read_tasks():
    tasks = []

    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            tasks.append(row)

    return tasks


# ---------------------------
# WRITE TASKS
# ---------------------------
def write_tasks(tasks):

    with open(CSV_FILE, mode="w", newline="") as file:

        fieldnames = [
            "id",
            "task",
            "priority",
            "due_date",
            "status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for task in tasks:
            writer.writerow(task)


# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def index():

    search = request.args.get("search", "")

    tasks = read_tasks()

    if search:
        tasks = [
            task for task in tasks
            if search.lower()
            in task["task"].lower()
        ]

    return render_template(
        "index.html",
        tasks=tasks,
        search=search
    )


# ---------------------------
# ADD TASK
# ---------------------------
@app.route("/add", methods=["POST"])
def add_task():

    tasks = read_tasks()

    if tasks:
        new_id = int(tasks[-1]["id"]) + 1
    else:
        new_id = 1

    task_data = {
        "id": str(new_id),
        "task": request.form["task"],
        "priority": request.form["priority"],
        "due_date": request.form["due_date"],
        "status": "Pending"
    }

    tasks.append(task_data)

    write_tasks(tasks)

    return redirect("/")


# ---------------------------
# DELETE TASK
# ---------------------------
@app.route("/delete/<task_id>")
def delete_task(task_id):

    tasks = read_tasks()

    tasks = [
        task
        for task in tasks
        if task["id"] != task_id
    ]

    write_tasks(tasks)

    return redirect("/")


# ---------------------------
# COMPLETE TASK
# ---------------------------
@app.route("/complete/<task_id>")
def complete_task(task_id):

    tasks = read_tasks()

    for task in tasks:

        if task["id"] == task_id:

            if task["status"] == "Pending":
                task["status"] = "Completed"
            else:
                task["status"] = "Pending"

    write_tasks(tasks)

    return redirect("/")


# ---------------------------
# EDIT PAGE
# ---------------------------
@app.route("/edit/<task_id>")
def edit_page(task_id):

    tasks = read_tasks()

    for task in tasks:

        if task["id"] == task_id:

            return render_template(
                "edit.html",
                task=task
            )

    return redirect("/")


# ---------------------------
# UPDATE TASK
# ---------------------------
@app.route("/update/<task_id>", methods=["POST"])
def update_task(task_id):

    tasks = read_tasks()

    for task in tasks:

        if task["id"] == task_id:

            task["task"] = request.form["task"]
            task["priority"] = request.form["priority"]
            task["due_date"] = request.form["due_date"]

    write_tasks(tasks)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)