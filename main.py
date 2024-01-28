from flask import Flask, render_template, request, jsonify
from calculatestars import StarCounter
from ChatBot.chatapp import chat_bot
from dotenv import load_dotenv

gpt_bot = chat_bot()

load_dotenv()

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

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def getMessage():
    posted_data = request.json
    message = posted_data.get("message")

    bot = chat_bot()
    response = bot.run_conversation(message)

    return jsonify({'response': response})

@app.route("/school")
def school():
    stars = 4.25

    star_counter = StarCounter()

    star_counter.count_stars(stars)
    counts = star_counter.get_counts()
    
    return render_template("school.html", school="UMBC", fullstars=counts["Full Stars"], halfstar=counts["Half Star"], emptystars=counts["Empty Stars"])

@app.route("/posts")
def posts():
    school = "UMBC"

    stars = 4.25

    star_counter = StarCounter()

    star_counter.count_stars(stars)
    counts = star_counter.get_counts()

    userdata = { "johndoe" : {
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123",
        "reviews": [
            {
            "school": "Springfield High School",
            "date": "2024-01-20",
            "review": "3.5",
            "comment": "Great experience and learning environment.",
            },
            {
            "school": "Green Valley College",
            "date": "2023-12-15",
            "review": "2",
            "comment": "Great experience and learning environment.",
            },
            {
            "school": "UMBC",
            "date": "2023-11-10",
            "review": "4.5",
            "comment": "Great experience with their disibility services and learning environment.",
            }
        ]
    },
    "boohoo" : {
        "first_name": "Boo",
        "last_name": "Hoo",
        "password": "password123",
        "reviews": [
            {
            "school": "Springfield High School",
            "date": "2034-05-22",
            "review": "4",
            "comment": "I LOVE IT HAD A experience and learning environment.",
            },
            {
            "school": "UMBC",
            "date": "2021-22-15",
            "review": "4.0",
            "comment": "I LOVE IT HAD A Great experience and learning environment.",
            },
            {
            "school": "Riverside University",
            "date": "2023-15-10",
            "review": "5",
            "comment": "I LOVE IT HAD A Great experience and learning environment.",
            }
        ]
    },
}


    return render_template("posts.html", userdata=userdata, school=school, fullstars=counts["Full Stars"], halfstar=counts["Half Star"], emptystars=counts["Empty Stars"])