# app.py
from flask import Flask, render_template, request, jsonify
import openai
from textblob import TextBlob
from googletrans import Translator

app = Flask(__name__)

# Configure your OpenAI API key
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_text', methods=['POST'])
def generate_text():
    user_input = request.form.get('prompt')

    # Create a killer prompt by providing some context and user input
    killer_prompt = f"Please generate a text based on the following input: {user_input}\nKiller prompt:"

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Choose the engine that suits your needs
            prompt=killer_prompt,
            max_tokens=200  # Adjust the number of tokens as needed
        )
        generated_text = response.choices[0].text

        # Sentiment analysis with TextBlob
        sentiment_analysis = TextBlob(generated_text)
        sentiment = sentiment_analysis.sentiment.polarity
        emotion = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"

        return jsonify({"response": generated_text, "sentiment": sentiment, "emotion": emotion})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    target_lang = request.form.get('target_lang')

    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang).text

    return jsonify({"translated_text": translated_text})

if __name__ == '__main__':
    app.run(debug=True)
