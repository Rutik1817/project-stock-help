from flask import Flask, render_template, request
import google.generativeai as palm
import os
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# Configure PALM API key
palm_api_key = os.environ["PALM_API_KEY"]
palm.configure(api_key=palm_api_key)

# Create Flask application instance
app = Flask(__name__)

# Define route for the home page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["post"])
def chatbot():
    user_input = request.form["message"]
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name

    prompt = f"user: {user_input}\nPaLM Bot:"

    # Generate response
    response = palm.generate_text(
        model=model,
        temperature=0,
        prompt=prompt,
        max_output_tokens=10000
        
    )
    bot_response = response.result 

    chat_history = []
    chat_history.append(f"user: {user_input}\nPaLM Bot: \n{bot_response}")

    # Return the rendered template with the response data
    return render_template("chatbot.html", user_input=user_input, bot_response=bot_response, chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
