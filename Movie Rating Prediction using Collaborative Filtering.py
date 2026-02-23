
#import librries
import pandas as pd
import numpy as np
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split, cross_validate
import matplotlib.pyplot as plt
import seaborn as sns

#load dataset
df = pd.read_csv('d:/python_ka_chilla/AI Projects/Movie Rating Prediction using Collaborative Filtering/ratings.csv')
df.drop('timestamp', axis=1, inplace=True)

# display first few rows of the dataset
print("Movie Ratings DataSet:\n", df.head())

#reader object for surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

#split the dataset into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

#train an SVD model
model = SVD()
model.fit(trainset)

#make predictions on the test set
predictions = model.test(testset)

#evaluate the model
rmse = accuracy.rmse(predictions)
print("Model Evaluation Results:")
print("RMSE:", rmse)

#make predictions for a specific user
user_id = 1
movie_ids = df['movieId'].unique()
predicted_ratings = [model.predict(user_id, movie_id).est for movie_id in movie_ids]
predicted_ratings_df = pd.DataFrame({'movieId': movie_ids, 'predicted_rating': predicted_ratings})
top_recommendations = predicted_ratings_df.sort_values(by='predicted_rating', ascending=False).head(10)
print(f"\nTop 10 movie recommendations for user {user_id}:\n", top_recommendations)

#visualization of predicted ratings distribution
plt.figure(figsize=(10,6))
sns.histplot(predicted_ratings, bins=20, kde=True)
plt.title('Distribution of Predicted Ratings')
plt.xlabel('Predicted Rating')
plt.ylabel('Frequency')
plt.show()

