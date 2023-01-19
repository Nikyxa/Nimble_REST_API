import os
from flask import Flask, render_template, request, redirect, send_file
from helper import list_all_files, download, upload
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = "upload_files"
BUCKET = "nimblebuckettest"


@app.route("/")
def index():
    return "It's a test service for Nimble."


@app.route("/files")
def files():
    contents = list_all_files(BUCKET)
    return render_template("files.html", contents=contents)


@app.route("/upload", methods=["POST"])
def upload_files():
    if request.method == "POST":
        f = request.files["file"]
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload(f"upload_files/{f.filename}", BUCKET, f.filename)
        return redirect("/files")


@app.route("/download/<filename>", methods=["GET"])
def download_files(filename):
    if request.method == "GET":
        output = download(filename, BUCKET)
        return send_file(output, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
