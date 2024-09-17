from flask import Flask, render_template
import subprocess

skills_app = Flask(__name__)

@skills_app.route("/")
def homepage():
    return render_template("index.html",
                           pagetitle="HomePage",
                           head="Welcome to the Maze!",
                           description="This is a monsters maze where you can enjoy playing")

@skills_app.route("/start_game", methods=["POST"])
def start_game():
        subprocess.Popen(['python', 'file_1.py'])    

if __name__ == "__main__":
    skills_app.run(debug=True)
