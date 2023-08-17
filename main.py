import os
import tempfile

from flask import Flask, render_template, request, send_file
from pdf2docx import Converter

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return "Nenhum arquivo enviado"

        pdf_file = request.files["pdf_file"]
        if pdf_file.filename == "":
            return "Nenhum arquivo selecionado"

        if pdf_file:
            pdf_filename = pdf_file.filename
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
            pdf_file.save(pdf_path)

            docx_filename = os.path.splitext(pdf_filename)[0] + ".docx"
            docx_path = os.path.join(app.config["UPLOAD_FOLDER"], docx_filename)

            convert_pdf_to_docx(pdf_path, docx_path)

            return send_file(docx_path, as_attachment=True)

    return render_template('index.html')


def convert_pdf_to_docx(pdf_path, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
