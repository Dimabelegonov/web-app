from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"
PROCESSED_FOLDER = "processed/"

# Убедитесь, что папки для загрузок и обработанных файлов существуют
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file and file.filename.endswith(".xlsx"):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return render_template("process.html", filename=file.filename)
    else:
        return "Only .xlsx files are allowed"


@app.route("/process/<filename>", methods=["POST"])
def process_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Пример обработки: просто добавим новый столбец с данными
    df = pd.read_excel(file_path)
    df["Processed"] = df[df.columns[0]] * 2  # Пример обработки

    processed_file_path = os.path.join(PROCESSED_FOLDER, f"processed_{filename}")
    df.to_excel(processed_file_path, index=False)

    return render_template("download.html", processed_file=f"processed_{filename}")


@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
