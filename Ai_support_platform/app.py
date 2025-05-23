from flask import Flask, render_template, request, redirect
from utils import process_text_and_store
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    text = request.form["company_data"]
    process_text_and_store(text)
    return "<h3>Data processed and stored successfully. You can now use it in chatbot.</h3>"

if __name__ == "__main__":
    if not os.path.exists("chroma_db"):
        os.mkdir("chroma_db")
    app.run(debug=True)

