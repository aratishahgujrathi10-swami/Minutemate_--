from flask import Flask, jsonify, render_template

from flask import Flask, jsonify
from recorder import Recorder
from transcriber import transcribe
from nlp import process
from flask import render_template
app = Flask(__name__)
status = {"recording": False}
minutes = {}
@app.route("/")
def home():
    return render_template("index.html")



@app.route("/start")
def start():
    status["recording"] = True
    recorder = Recorder()
    path = recorder.record()
    text = transcribe(path)
    minutes["latest"] = process(text)
    status["recording"] = False
    return jsonify({"message": "Recording complete"})

@app.route("/status")
def get_status():
    return jsonify({"status": "recording" if status["recording"] else "idle"})
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/minutes/latest")
def get_minutes():
    return jsonify(minutes.get("latest", {}))

if __name__ == "__main__":
    app.run(debug=True)

    from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/minutes/sample", methods=["GET"])
def get_sample_minutes():
    return jsonify({
        "summary": "Team discussed proposal updates, vendor finalization, meeting scheduling, and timeline reviews.",
        "action_items": [
            "John will send out the updated proposal.",
            "We need to finalize the vendor list.",
            "Sarah, please schedule a follow-up meeting.",
            "Everyone should review the project timeline."
        ],
        "reminders": [
            "Monday",
            "this week",
            "Friday",
            "Thursday"
        ]
    })

