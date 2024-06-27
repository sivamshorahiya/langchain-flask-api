""" EXPLANATION:
    This is a simple Flask API server that uses the LangChain pipeline to answer questions.
    The server listens for POST requests to the /ask endpoint with a JSON payload containing a question.
    The server then uses the LangChain pipeline to generate an answer to the question and returns it in the response.
    
    To set API_KEY, use the following command:
    'setx OPENAI_API_KEY your_api_key_here' for Windows
    'export OPENAI_API_KEY=your_api_key_here' for Linux

    To run the server, use the following command:
    'python server.py'
    To test the server, use the following command:
    'curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d "{\"question\": \"What is the capital of France?\"}"'
"""

from flask import Flask, request, jsonify
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

app = Flask(__name__)

model = ChatGoogleGenerativeAI(model="gemini-pro")
# model = ChatOpenAI(model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant for students. Answer the following question: {question}"
)

chain = prompt | model | StrOutputParser()

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        response = chain.invoke({"question": question})
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    