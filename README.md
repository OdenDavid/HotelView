HotelView: Intelligent Hotel Review Analysis
=============================================

Overview
-----------
HotelView is a web application leveraging sentiment analysis and topic modeling to determine customer satisfaction and dissatisfaction factors based on hotel reviews.

Project Structure
-------------------
```
HotelView
├── Images
├── Models
│   ├── random_forest.joblib
│   ├── tfidf_vectorizer.joblib
│   └── topic_model
├── UserApp.py
├── AdminApp.py
├── data_topics.csv
├── Data.db
├── Datafiniti_Hotel_Reviews_Jun19.csv
├── explore.ipynb
├── hotels.csv
├── NLTK_download.py
├── preprocess.py
├── requirements.txt
├── Sentiment.py
└── Topic.py
```

Methodology
--------------
Data Collection
  * Datafiniti's Business Database (1,000 hotels, reviews, ratings, locations)
Descriptive Statistics
  * Hotel count
  * Top 10 hotels by rating
  * Review distribution
Data Visualization
  * Word Cloud
  * Top 10 hotels with 5-star rating (Bar Chart)
  * Number of reviews over time (Line Plot)
  * Top cities (Sunburst Chart)
  * Average ratings by province (Choropleth Map)
Data Preprocessing
  * Dropping empty rows
  * Cleaning reviews
Sentiment Analysis
  * Blob
  * Vader
  * User rating
Topic Modeling
  * Latent Dirichlet Allocation (LDA)
  * BERTopic
  * Intertopic distance maps
  Topic grouping (5 categories)

Features
------------
User App
  * Search hotels by location or name
  * View reviews categorized by sentiment (Positive, Negative, Neutral)
  * Submit own reviews
  * Filter reviews by rating, date, and username
AdminApp
  * Real-time review analysis dashboard
  * Total Reviews
  * Sentiment Distribution (Positive, Negative, Neutral)
  * Interactive Pie Chart
  * Word Cloud (most commonly used words)
  * Topic Analysis:
    - Guest Complaints and Hotel Issues
    - Positive Guest Experiences and Hotel Amenities
    - Noise and Comfort Considerations in Accommodations
    - Hotel Guest Feedback and Interactions

Technologies Used
--------------------
  * Python
  * Natural Language Processing (NLTK, spaCy)
  * Machine Learning (Scikit-learn, TensorFlow)
  * Web Development (Flask, React)
  * Database Management (MongoDB)
  * Data Visualization (Matplotlib, Seaborn)

Installation
---------------
  * Clone repository: git clone https://github.com/your-username/HotelView.git
  * Install dependencies: pip install -r requirements.txt
  * Run User App: python UserApp.py
  * Run AdminApp: python AdminApp.py

Contributing
------------
Contributions welcome! Please open an issue or submit a pull request.

Author
--------
David Oden
