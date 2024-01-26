from flask import Flask, render_template, request, jsonify
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

app = Flask(__name__)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = ""

# Load documents and create QA system
loader = PyPDFLoader("48lawsofpower.pdf")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    query = data.get('query', '')

    if query.lower() == "quit":
        return jsonify({'result': 'Goodbye!'})

    if query == "":
        return jsonify({'result': 'Please enter a valid question.'})

    result = qa({"query": query})
    return jsonify({'result': result['result']})

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=int("5000"),debug=True)
