from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np

from app.db import load_data_from_db

data = load_data_from_db()
texts = [row[1] for row in data]
ids = [row[0] for row in data]
categories = [row[2] for row in data]

# Descargar recursos de NLTK
nltk.download('punkt')
nltk.download('stopwords')

stop_words = {
    'en': set(stopwords.words('english')),
    'es': set(stopwords.words('spanish')),
}

stemmers = {
    'en': SnowballStemmer('english'),
    'es': SnowballStemmer('spanish'),
}


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def preprocess_text(text, language):
    if (language not in stop_words) or (language == "unknown"):
        return text
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words[language]]
    stemmed_tokens = [stemmers[language].stem(token) for token in tokens]
    return " ".join(stemmed_tokens)


# Crear el vectorizador TF-IDF y ajustar con los textos preprocesados
def create_vectorizer(texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix


vectorizer, tfidf_matrix = create_vectorizer([preprocess_text(text, detect_language(text)) for text in texts])


def get_predictions(processed_input, texts, ids):
    user_vector = vectorizer.transform([processed_input])
    cosine_similarities = np.dot(user_vector, tfidf_matrix.T).toarray()
    top_similar_indices = cosine_similarities.argsort(axis=1)[0][::-1]
    seen_texts = set()
    predictions = []
    for i in top_similar_indices:
        if texts[i] not in seen_texts:
            seen_texts.add(texts[i])
            predictions.append({"id": ids[i], "text": texts[i].strip()})
        if len(predictions) == 3:
            break
    return predictions
