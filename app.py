from flask import Flask, render_template, request, send_from_directory, redirect
import os

app = Flask(__name__)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        if 'image' not in request.files:
            return "No file uploaded"
        file = request.files['image']
        file.save(f"uploads/{file.filename}")

    images = os.listdir("uploads")

    return render_template("index.html", images=images)

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/uploads/<filename>/see")
def download_file(filename):
    code = "<a href='/uploads/" + filename + "/see/url'><img src='/uploads/" + filename + "/see/url' alt='unable to upload'></a><br><br><a href='/upload/" + filename + "/delete'>delete the file</a>"
    return render_template("see.html", code=code, file_name=filename)

@app.route("/upload/<filename>/delete")
def delete_file(filename):
    os.remove(f"uploads/{filename}")
    return redirect("/", code=302)

@app.route("/uploads/<filename>/see/url")
def file_url(filename):
    return send_from_directory("uploads", filename)

app.run(debug=True, host="0.0.0.0", port=5500)