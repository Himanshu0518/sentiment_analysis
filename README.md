# 🎬 Sentiment Analysis on Movie Reviews

This project performs sentiment analysis on movie reviews to determine whether a given review is **positive**, **negative**, or **neutral**. It uses Natural Language Processing (NLP) techniques and a machine learning model trained on labeled review data.

## 📌 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Approach](#approach)
- [Model Architecture](#model-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Future Work](#future-work)
- [Project Structure](#project-structure)
- [License](#license)

---

## 🧠 Overview

Movie reviews can give deep insights into viewer opinions. This project analyzes textual movie reviews and predicts their sentiment. It is useful for:

- Understanding audience reception.
- Monitoring public sentiment about films.
- Powering review aggregation platforms.

---

## 📊 Dataset

- **Name:** IMDb Movie Reviews Dataset +  Rotten Tomato dataset
- **Size:** ~1,00,000 reviews
- **Classes:** `Positive`, `Negative`)*
- **Source:**  [IMDB Dataset](https://www.kaggle.com/datasets/vishakhdapat/imdb-movie-reviews) +  [Rotten Tomato Dataset]( https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset)

---

## ⚙️ Approach

1. **Text Preprocessing**
   - Handling NULL values , empty strings
   - Lowercasing
   - Removing punctuation and stopwords
   - Tokenization
   - Stemming

2. **Feature Extraction**
   -  Embedding Layer

3. **Model**
   - LSTM RNN 

4. **Evaluation**
   - Accuracy, Precision, Recall, F1-score
   - Confusion Matrix

---

# 📈 Results

    """"
               precision    recall  f1-score   support

    Negative       0.87      0.85      0.86      4961
    Positive       0.86      0.88      0.87      5039

    accuracy                           0.86     10000
    macro avg       0.86      0.86      0.86     10000
    weighted avg    0.86      0.86      0.86     10000

    """"