from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Dummy dataset 
tweets = [
    "Hurricane warning in Florida",
    "Tornado spotted in Kansas",
    "Earthquake shakes California",
    "Flooding in downtown after heavy rain",
    "Wildfire spreads rapidly in Colorado"
]

# test with something like "Earthquakes in Japan", "Fires in California"

labels = ["hurricane", "flood", "fire", "earthquake", "unrelated"]

# Simple text classification pipeline 
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()), 
    ('classifier', MultinomialNB())
])

# Train the model 
pipeline.fit(tweets, labels) 

# Save the dummy model 
joblib.dump(pipeline, 'api/dummy_model.pkl')