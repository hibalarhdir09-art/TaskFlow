
from flask import Flask, render_template, request, redirect, url_for, send_file
from azure_storage import upload_file, download_file, delete_file, list_files
from email_service import send_email
import os

app = Flask(__name__)

# Temporary storage for tasks
tasks = []

# Temporary notification email
notification_email = ""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        deadline_date = request.form.get("deadline_date")
        deadline_time = request.form.get("deadline_time")

        if title and deadline_date and deadline_time:

            task = {
                "title": title,
                "description": description,
                "deadline_date": deadline_date,
                "deadline_time": deadline_time
            }

            tasks.append(task)

        return redirect(url_for("home"))

    files = list_files()

    return render_template(
        "index.html",
        tasks=tasks,
        files=files,
        notification_email=notification_email
    )


# Save notification email and send confirmation
@app.route("/save_email", methods=["POST"])
def save_email():

    global notification_email

    email = request.form.get("email", "").strip()

    if "@" in email and "." in email.rsplit("@", 1)[-1]:

        notification_email = email

        # Send confirmation email using Azure Communication Services
        send_email(
            receiver_email=notification_email,
            subject="TaskFlow - Email Notifications",
            message_content=(
                "Hello!\n\n"
                "Your email address has been registered successfully "
                "in TaskFlow.\n\n"
                "You will be able to receive task notifications "
                "through this email address.\n\n"
                "TaskFlow Team"
            )
        )

    return redirect(url_for("home"))


# Delete a task
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)

    return redirect(url_for("home"))


# Upload a file to Azure Blob Storage
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    if file and file.filename:
        upload_file(file, file.filename)

    return redirect(url_for("home"))


# Download a file from Azure Blob Storage
@app.route("/download/<filename>")
def download(filename):

    destination = os.path.join("downloads", filename)

    os.makedirs("downloads", exist_ok=True)

    download_file(filename, destination)

    return send_file(destination, as_attachment=True)


# Delete a file from Azure Blob Storage
@app.route("/delete_file/<filename>", methods=["POST"])
def delete_blob(filename):

    delete_file(filename)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
