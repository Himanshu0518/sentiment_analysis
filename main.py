from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid thread issues
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import tensorflow 

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Disable GPU for TensorFlow (optional)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# Disable oneDNN custom operations to avoid warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

app = Flask(__name__)

# Load pre-trained model
model = load_model('movie_reviews_model.keras')

# Load NLTK resources
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# Load pre-trained tokenizer
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Define max_length (should match the value used during training)
max_length = 100

# Preprocessing function (includes HTML tag removal, stopwords, stemming)
def preprocess_text(text):
    if isinstance(text, str):
        text = re.sub('[^a-zA-Z]', ' ', text)  # Remove punctuation
        text = text.lower()
        
        # Remove stopwords and apply stemming
        words = text.split()
        filtered_words = [ps.stem(word) for word in words if word not in stop_words]
        return ' '.join(filtered_words)
    return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == "POST":
        try:
            if "file" not in request.files or request.files["file"].filename == "":
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            data = pd.read_csv(file, engine='python') 

            if 'Reviews' not in data.columns:
                return jsonify({'error': 'No "Reviews" column found in the uploaded file'}), 400

            reviews = data['Reviews'].dropna().apply(preprocess_text)
            
            if len(reviews) == 0:
                return jsonify({'error': 'No valid reviews found in the file'}), 400

            # Use pre-trained tokenizer (DO NOT fit a new tokenizer)
            sequences = tokenizer.texts_to_sequences(reviews)
            padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

            predictions = model.predict(padded_sequences)

            pos_reviews = np.sum(predictions > 0.5)
            neg_reviews = np.sum(predictions <= 0.5)

            # Generate WordCloud
            text = ' '.join(reviews)
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
            img = io.BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(img, format='png')
            plt.close()  # Close the figure to free memory
            img.seek(0)
            wordcloud_url = base64.b64encode(img.getvalue()).decode()

            # Generate Pie Chart
            fig, ax = plt.subplots()
            labels = ['Positive', 'Negative']
            sizes = [int(pos_reviews), int(neg_reviews)]
            colors = ['#66b3ff', '#ff9999']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')

            pie_img = io.BytesIO()
            plt.savefig(pie_img, format='png')
            plt.close(fig)  # Close the figure to free memory
            pie_img.seek(0)
            pie_chart_url = base64.b64encode(pie_img.getvalue()).decode()

            return jsonify({
                'wordcloud': wordcloud_url,
                'pie_chart': pie_chart_url,
                'positive_count': int(pos_reviews),
                'negative_count': int(neg_reviews),
                'total_reviews': len(reviews)
            })

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_sentiment():
    if request.method == "POST":
        try:
            text = request.form.get('custom-text', '').strip()
            if not text:
                return jsonify({'error': "Please enter valid text for sentiment analysis."})
            
            print(text)
            analyzer = SentimentIntensityAnalyzer()
            sentiment_scores = analyzer.polarity_scores(text)
            sentiment_result = {
                'positive': sentiment_scores['pos'],
                'negative': sentiment_scores['neg'],
                'neutral': sentiment_scores['neu'],
                'compound': sentiment_scores['compound']
            }
            return jsonify({'sentiment': sentiment_result})

        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
