from flask import Flask, render_template
from calculatestars import StarCounter

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/school")
def school():
    stars = 1.7

    star_counter = StarCounter()

    star_counter.count_stars(stars)
    counts = star_counter.get_counts()
    
    return render_template("school.html", school="UMBC", fullstars=counts["Full Stars"], halfstar=counts["Half Star"], emptystars=counts["Empty Stars"])