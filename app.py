from ml.detect_change import detect_change
from werkzeug.utils import secure_filename
from PIL import Image


from flask import Flask, render_template, request, redirect, url_for
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULT_FOLDER"], exist_ok=True)
# Welcome page
@app.route("/")
def index():
    return render_template("index.html")


# Upload form page
@app.route("/upload")
def upload():
    return render_template("form.html")


# Detection route (logic will be added later)
@app.route("/detect", methods=["POST"])
def detect():
    before_image = request.files.get("before_image")
    after_image = request.files.get("after_image")

    if not before_image or not after_image:
        return "Both images are required", 400

    before_name = secure_filename(before_image.filename)
    after_name = secure_filename(after_image.filename)

    before_path = os.path.join(app.config["UPLOAD_FOLDER"], before_name)
    after_path = os.path.join(app.config["UPLOAD_FOLDER"], after_name)

    before_image.save(before_path)
    after_image.save(after_path)

    if not is_valid_image(before_path) or not is_valid_image(after_path):
        os.remove(before_path)
        os.remove(after_path)
        return "Invalid image file", 400

    result_name = f"result_{before_name}"
    result_path = os.path.join(app.config["RESULT_FOLDER"], result_name)

    result_path, change_percentage = detect_change(
    before_path, after_path, result_path
    )
    # Save copies of original images into results folder
    before_result_name = f"before_{before_name}"
    after_result_name = f"after_{after_name}"

    before_result_path = os.path.join(app.config["RESULT_FOLDER"], before_result_name)
    after_result_path = os.path.join(app.config["RESULT_FOLDER"], after_result_name)

    os.replace(before_path, before_result_path)
    os.replace(after_path, after_result_path)


    

    return render_template(
    "result.html",
    before_image=before_result_name,
    after_image=after_result_name,
    result_image=result_name,
    change_percentage=change_percentage
)





def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    app.run(debug=True)
