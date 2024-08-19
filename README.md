# RAG-ChatBot-Using-GROQ

This project enables users to ask questions from PDF files and get answers using GROQ LLM, a conversational AI model. The project utilizes HTML, CSS, Bootstrap and JavaScript for the user interface and various libraries for text extraction, vectorization, and question-answering.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/01Prashant/RAG-ChatBot-Using-GROQ.git
   cd RAG-ChatBot-Using-GROQ

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt

## Usage

1. **Run the Flask app:**

   ```sh
   python app.py

2. Access the app in your web browser by navigating to the provided URL.
3. Ask questions from the uploaded PDF files by typing them into the text input field and clicking "Send".

## How It Works

1. The app allows users to upload PDF files.
2. Upon submission, the text is extracted from the PDF files.
3. The text is split into chunks and vectorized using chromaDB default embedding model: 'all-MiniLM-L6-v2'.
4. Conversational AI model GROQ is employed for question-answering.
5. Users can ask questions related to the content of the PDF files, and the app provides answers based on the provided context.

## Configuration

Ensure you have set up a GROQ API key and added it to your environment variables (`GROQ_API_KEY`).

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests.
