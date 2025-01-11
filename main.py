from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


app = Flask(__name__)
model = load_model('movie_reviews_model.keras')


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()


tokenizer = Tokenizer(num_words = 5000, oov_token="<OOV>")
max_length = 100

# Preprocessing function (includes HTML tag removal, stopwords, stemming)
def preprocess_text(text):
  #  text = BeautifulSoup(text, "html.parser").get_text()  # Remove HTML tags
    text = re.sub('[^a-zA-Z]',' ', text)  # Remove punctuation
    text = text.lower()
    
    # Remove stopwords and apply stemming
    words = text.split()
    filtered_words = [ps.stem(word) for word in words if word not in stop_words]
    return ' '.join(filtered_words)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file'] 
        data = pd.read_csv(file,engine='python') 
        reviews = data['Reviews'].apply(preprocess_text)
        tokenizer.fit_on_texts(reviews) 

        sequences = tokenizer.texts_to_sequences(reviews)
        padded_sequences = pad_sequences(sequences, maxlen=max_length ,  padding='post', truncating='post')
        predictions = model.predict(padded_sequences)
       
        print("Predictions:", predictions)

        pos_reviews = np.sum(predictions > 0.5)
        neg_reviews = np.sum(predictions <= 0.5)

        
        # Generate WordCloud
        text = ' '.join(reviews)
        wordcloud = WordCloud(width=800, height=400).generate(text)
        img = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(img, format='png')
        img.seek(0)
        wordcloud_url = base64.b64encode(img.getvalue()).decode()

        # Generate Pie Chart
        fig, ax = plt.subplots()
        labels = ['Positive', 'Negative']
        sizes = [pos_reviews, neg_reviews]
        colors = ['#66b3ff', '#ff9999']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        pie_img = io.BytesIO()
        plt.savefig(pie_img, format='png')
        pie_img.seek(0)
        pie_chart_url = base64.b64encode(pie_img.getvalue()).decode()

        return jsonify({
            'wordcloud': wordcloud_url ,
            'pie_chart': pie_chart_url
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/predict', methods=['POST'])
def predict_sentiment():
    text = request.form['custom-text']

    
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores  = analyzer.polarity_scores(text)  
    sentiment_result = {
        'positive': sentiment_scores['pos'],
        'negative': sentiment_scores['neg'],
        'neutral': sentiment_scores['neu'],
        'compound': sentiment_scores['compound']
    }
    return jsonify({'sentiment': sentiment_result})

if __name__ == "__main__":
    app.run(debug=True)
