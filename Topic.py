from bertopic import BERTopic
import preprocess

# Load the topic model
topic_model = BERTopic.load("Models/topic_model")	

import warnings
warnings.filterwarnings("ignore")

def get_topic(review: str):
    
    review_cleaned = preprocess.review_clean_lematize_vectorize(review, topic=True)

    similar_topics, similarity = topic_model.find_topics(review_cleaned, top_n=1)

    Cluster1 = [6,14,25,30] # Guest Complaints and Hotel Issues
    Cluster2 = [2,5,8,10,15,17,24,26,27,31] # Positive Guest Experiences and Hotel Amenities
    Cluster3 = [7,13,28,32,33] # Noise and Comfort Considerations in Accommodations
    Cluster4 = [0,4,9,11,12,19,20,21,22,23,29,1,3,16,18] # Hotel Guest Feedback and Interactions

    topic = similar_topics[0]

    if topic == -1:
        topic_text = "Others"
    elif topic in Cluster1:
        topic_text = "Guest Complaints and Hotel Issues"
    elif topic in Cluster2:
        topic_text = "Positive Guest Experiences and Hotel Amenities"
    elif topic in Cluster3:
        topic_text = "Noise and Comfort Considerations in Accommodations"
    elif topic in Cluster4:
        topic_text = "Hotel Guest Feedback and Interactions"
    else:
        pass

    return topic_text