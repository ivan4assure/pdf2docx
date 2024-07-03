from flask import Flask, request, render_template, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica si el archivo PDF fue subido
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            # Guarda el archivo PDF en la carpeta de uploads
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)

            # Define el nombre del archivo DOCX de salida
            docx_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.docx')

            # Convierte el archivo PDF a DOCX
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            # Envía el archivo DOCX convertido al usuario
            return send_file(docx_path, as_attachment=True)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
