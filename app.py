from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Feedback
from summarizer import summarize_text
from flask_migrate import Migrate
import os
import pickle

# Load the pickled model
with open("nlp_model.pkl", "rb") as file:
    nlp = pickle.load(file)

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://feedback_0gek_user:ZZx8fzM6xWE1kQDWmYA1Zll6g3OLMtAi@dpg-cua8cjtds78s739l8320-a.oregon-postgres.render.com/feedback_0gek"
#"postgresql://neondb_owner:npg_0FwMV3fKvmuz@ep-dry-flower-a1l5zs73-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'lakshmi'  

db.init_app(app)
migrate = Migrate(app, db)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_text = request.form["input_text"]
        summarized_text = summarize_text(input_text)
        return render_template("summary.html", input_text=input_text, summarized_text=summarized_text)
    return render_template("index.html")

@app.route("/feedback", methods=["POST"])
def feedback():
    name = request.form["name"]
    rating = int(request.form["rating"])
    input_text = request.form["input_text"]
    summarized_text = request.form["summarized_text"]
    feedback_text = request.form["feedback"]

    # Add feedback to the database
    feedback_entry = Feedback(
        name=name,
        rating=rating,
        input_text=input_text,
        summarized_text=summarized_text,
        feedback=feedback_text
    )
    db.session.add(feedback_entry)
    db.session.commit()

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
