import preprocess
import joblib

loaded_rf = joblib.load("Models/random_forest.joblib")

def get_sentiment(review: str):
    """predict sentiment from text review"""

    X = preprocess.review_clean_lematize_vectorize(review)
    response = loaded_rf.predict(X)

    # return new_sentiment

    if response[0] == 0:
        response = "Negative"
    elif response[0] == 1:
        response = "Neutral"  
    elif response[0] == 2:
        response = "Positive"
        
    return response