from flask import Flask, render_template, request
import smtplib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

posts = requests.get("https://api.npoint.io/f8b95cc5bbc3f353fa13").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(os.environ["my_email"], password=os.environ["password"])
        connection.sendmail(os.environ["my_email"], "brianpaykani@yahoo.com", email_message)


if __name__ == "__main__":
    app.run(debug=True)
