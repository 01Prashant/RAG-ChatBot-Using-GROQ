from working import get_text_from_pdf, get_text_chunks, embeddingStore, loadCollection, embeddingsQuery, generate
from flask import Flask, request, jsonify, render_template, Response
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
app     =   Flask(__name__)
client  =   Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'pdfFile' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        file = request.files['pdfFile']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        if file and file.filename.endswith('.pdf'):
            try:
                text    =   get_text_from_pdf(file)
                chunks  =   get_text_chunks(text)
                embeddingStore(chunks)
            except Exception as e:
                return jsonify({'message': e}), 400
            return jsonify({'message': 'File uploaded successfully'}), 200
        return jsonify({'message': 'Invalid file type'}), 400
    return render_template('home.html')


@app.route("/answer", methods=["GET", "POST"])
def answer():
    data                =   request.get_json()
    user_question       =   data["message"]
    if not user_question:
        return jsonify({'message': 'No message provided'}), 400
    print(user_question)
    collection          =   loadCollection()
    if collection:
        revlevantText   =   embeddingsQuery(user_question, collection)
        return Response(generate(revlevantText, user_question), content_type='text/plain; charset=utf-8')
    else:
        return jsonify({'message': 'No collection loaded. Please upload a file first.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
