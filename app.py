
from flask import Flask, request, render_template
from docx import Document
import re
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_data_from_docx(path):
    doc = Document(path)
    text = "\n".join([p.text for p in doc.paragraphs])

    # Procurar datas no formato dd/mm/aaaa ou dd-mm-aaaa
    date_match = re.search(r'\b(\d{2}[\/\-]\d{2}[\/\-]\d{4})\b', text)
    vencimento = date_match.group(1) if date_match else "Não encontrado"

    # Procurar condicionantes (exemplo: frases que contêm a palavra "condicionante")
    condicionantes = [line for line in text.split('\n') if "condicionante" in line.lower()]

    return {
        "vencimento": vencimento,
        "condicionantes": condicionantes
    }

@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "docFile" not in request.files:
        return "Arquivo não encontrado", 400

    file = request.files["docFile"]
    if file.filename == "":
        return "Nenhum arquivo selecionado", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    data = extract_data_from_docx(filepath)
    return render_template("upload.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
