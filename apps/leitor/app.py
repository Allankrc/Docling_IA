from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from docx import Document
import pdfplumber
import os
import re
import spacy

from models import Documento, Session

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
nlp = spacy.load("pt_core_news_sm")

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_data(text):
    # Regex para data (vencimento)
    date_match = re.search(r'\b(\d{2}[\/\-]\d{2}[\/\-]\d{4})\b', text)
    vencimento = date_match.group(1) if date_match else "Não encontrado"

    # Condicionantes: frases com palavras-chave
    doc = nlp(text)
    condicionantes = [
        sent.text.strip() for sent in doc.sents
        if "condicionante" in sent.text.lower()
        or "condição" in sent.text.lower()
        or "exigência" in sent.text.lower()
    ]

    return vencimento, condicionantes

@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("docFile")
    if not file or file.filename == "":
        return "Arquivo não selecionado", 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    # Extração de texto
    if filename.endswith(".docx"):
        text = extract_text_from_docx(path)
    elif filename.endswith(".pdf"):
        text = extract_text_from_pdf(path)
    else:
        return "Formato não suportado. Envie .docx ou .pdf", 400

    vencimento, condicionantes = extract_data(text)

    # Armazenar no banco
    session = Session()
    novo_doc = Documento(
        nome_arquivo=filename,
        data_vencimento=vencimento,
        condicionantes="\n".join(condicionantes)
    )
    session.add(novo_doc)
    session.commit()

    return render_template("upload.html", data={
        "vencimento": vencimento,
        "condicionantes": condicionantes
    })
