import re
import nltk
#from NLTK_download import download
#download()
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

wn = nltk.WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words('english')

tfidf_vectorizer = TfidfVectorizer()

def review_clean(review):
    # changing to lower case
    lower = review.lower()
    
    # Removing all the special Characters
    special_remove = lower.replace(r'[^\w\d\s]',' ')
    
    # Removing all the non ASCII characters
    ascii_remove = special_remove.replace(r'[^\x00-\x7F]+',' ')
    
    # Removing the leading and trailing Whitespaces
    whitespace_remove = ascii_remove.replace(r'^\s+|\s+?$','')
    
    # Replacing multiple Spaces with Single Space
    multiw_remove = whitespace_remove.replace(r'\s+',' ')

    # removing double quotesfrom string
    review_new = multiw_remove.strip('\"')
    
    return review_new


def review_clean_lematize_vectorize(review: str, topic = False):
    
    """Pre-Process Review"""
    review_cleaned = review_clean(review)

    extras = ["seattle","hyatt","san","francisco","orleans","diego","hampton","orlando","florida","chicago","philadelphia","atlanta",\
          "us","waikiki"]
    if topic:
        stopwords.extend(extras)

    no_stopwords = ' '.join([word for word in review_cleaned.split() if word not in stopwords])
    lemm_text = ''.join([wn.lemmatize(word) for word in no_stopwords])
    clean_text = lemm_text.strip()

    if topic:
        return clean_text
    else:
        tfidf_vectorizer = joblib.load("Models/tfidf_vectorizer.joblib")
        X = tfidf_vectorizer.transform([clean_text])
        return X