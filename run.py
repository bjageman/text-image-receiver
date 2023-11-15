import os
from flask import Flask, request, render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__, static_url_path="/static/")


@app.route("/")
def index():
    return render_template("index.html", title="Welcome")


@app.route("/sms", methods=["POST"])
def incoming_sms():
    sender = request.form.get("From")
    message = request.form.get("Body")
    media_url = request.form.get("MediaUrl0")
    print(f"{sender} sent {message}")
    if media_url:
        r = requests.get(media_url)
        content_type = r.headers["Content-Type"]
        username = sender
        if content_type == "image/jpeg":
            filename = f"static/latest.jpg"
        elif content_type == "image/png":
            filename = f"static/latest.png"
        elif content_type == "image/gif":
            filename = f"static/latest.gif"
        else:
            filename = None
        if filename:
            if not os.path.exists(f"static/{username}"):
                os.mkdir(f"static/{username}")
            with open(filename, "wb") as f:
                f.write(r.content)
            print("Thank you! Your image was received.")
        else:
            print("The file that you submitted is not a supported image type.")
    else:
        print("Please send an image!")
    resp = MessagingResponse()
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
