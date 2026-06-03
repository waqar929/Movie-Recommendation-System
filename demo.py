import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# Collaborative Filtering
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# Content-Based Filtering
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Evaluation Metrics
from sklearn.metrics import mean_squared_error

ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
links = pd.read_csv("links.csv")

print("LINKS COLUMNS:")
print(links.columns)

ratings.rename(columns={
    "userId": "user_id",
    "movieId": "movie_id"
}, inplace=True)

movies.rename(columns={
    "movieId": "movie_id"
}, inplace=True)

links.rename(columns={
    "movieId": "movie_id"
}, inplace=True)
print(links.head())

movies = movies[["movie_id", "title"]]

# Remove duplicates
ratings.drop_duplicates(inplace=True)
movies.drop_duplicates(inplace=True)

# Check missing values
print("\nMissing Values in Ratings:")
print(ratings.isnull().sum())

print("\nMissing Values in Movies:")
print(movies.isnull().sum())

# Merge data
data = pd.merge(ratings, movies, on="movie_id")

print("\nDataset Loaded Successfully!")
print(data.head())

reader = Reader(rating_scale=(1, 5))

dataset = Dataset.load_from_df(
    ratings[['user_id', 'movie_id', 'rating']],
    reader
)

# Train-test split
trainset, testset = train_test_split(
    dataset,
    test_size=0.2,
    random_state=42
)

# Train SVD model
model = SVD(
    n_factors=30,
    n_epochs=10,
    random_state=42
)

model.fit(trainset)

app = Flask(__name__)
CORS(app)
# =====================================
# TMDB API KEY
# =====================================

TMDB_API_KEY = "YOUR TMDB_API_KEY"

predictions = model.test(testset)

print("\nEvaluation Metrics:")

# RMSE
rmse = accuracy.rmse(predictions)

# MAE
mae = accuracy.mae(predictions)

# Convert predictions
actual = [pred.r_ui for pred in predictions]
predicted = [pred.est for pred in predictions]

# MSE
mse = mean_squared_error(actual, predicted)

print("MSE:", round(mse, 4))
print("RMSE:", round(rmse, 4))
print("MAE:", round(mae, 4))

metrics_names = ["MSE", "RMSE", "MAE"]
metrics_values = [mse, rmse, mae]

plt.figure(figsize=(8, 5))

plt.bar(metrics_names, metrics_values)

plt.title("Regression Evaluation Metrics")

plt.xlabel("Metrics")
plt.ylabel("Values")

# Show values on bars
for i, value in enumerate(metrics_values):
    plt.text(i, value + 0.01, round(value, 3), ha='center')

plt.show()

vectorizer = CountVectorizer(stop_words='english')

content_matrix = vectorizer.fit_transform(movies['title'])

content_similarity = cosine_similarity(content_matrix)


# Users from ratings
user_ids = ratings['user_id'].unique()

# Movies ONLY from ratings
movie_ids = ratings['movie_id'].unique()

# Filter movies dataframe
movies = movies[movies['movie_id'].isin(movie_ids)]

# Create mappings
user_map = {u: i for i, u in enumerate(user_ids)}
movie_map = {m: i for i, m in enumerate(movie_ids)}

# Create user-item matrix
matrix = np.zeros((len(user_ids), len(movie_ids)))

for row in ratings.itertuples():

    # Fill ratings
    matrix[
        user_map[row.user_id],
        movie_map[row.movie_id]
    ] = row.rating

# Get latent matrices
user_factors = model.pu
item_factors = model.qi

# IMPORTANT FIX
# Make dimensions equal
min_movies = min(len(movie_ids), item_factors.shape[0])

movie_ids = movie_ids[:min_movies]

matrix = matrix[:, :min_movies]

item_factors = item_factors[:min_movies]

# Final prediction matrix
pred_matrix = np.dot(user_factors, item_factors.T)

def recommend_movies(user_id, top_n=10):

    if user_id not in user_map:
        print("User not found")
        return []

    user_idx = user_map[user_id]

    # Get prediction scores
    scores = pred_matrix[user_idx].copy()

    # Remove watched movies
    watched = matrix[user_idx] > 0
    scores[watched] = -1
   
    top_indices = np.argsort(scores)[-50:]

    # Shuffle recommendations
    np.random.shuffle(top_indices)

    # Take top_n after shuffle
    top_indices = top_indices[:top_n]

    recommendations = []

    for idx in top_indices:

        movie_id = movie_ids[idx]

        movie_row = movies[
            movies['movie_id'] == movie_id
        ]

        if len(movie_row) > 0:

            title = movie_row['title'].values[0]

            predicted_rating = model.predict(
    user_id,
    int(movie_id)
).est

        recommendations.append(
    (title, round(predicted_rating, 2), int(movie_id))
)

    return recommendations

# CHANGE USER ID HERE
user_id = 10

# CHANGE NUMBER OF RECOMMENDATIONS HERE
top_n = 10

recommendations = recommend_movies(user_id, top_n)

print(f"\nTop {top_n} Recommendations for User {user_id}:\n")

for i, (title, score, movie_id) in enumerate(recommendations, 1):
   print(f"{i}. {title} --> Predicted Rating: {score}/5")



def get_movie_poster_by_id(movie_id):

    try:
        link_row = links[links["movie_id"] == int(movie_id)]

        if link_row.empty:
            print("No link found for movie_id:", movie_id)
            return None

        tmdb_id = link_row["tmdbId"].values[0]

        if pd.isna(tmdb_id):
            print("No TMDB ID for movie_id:", movie_id)
            return None

        tmdb_id = int(tmdb_id)

        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
        response = requests.get(url).json()

        poster_path = response.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        print("No poster path for tmdb_id:", tmdb_id)

    except Exception as e:
        print("Poster Error:", e)

    return None


@app.route('/recommend', methods=['GET'])
def get_recommendations():

    try:
        user_id = int(request.args.get('user_id'))
        top_n = int(request.args.get('top_n', 10))

        recommendations = recommend_movies(user_id, top_n)

        result = []

        for title, rating, movie_id in recommendations:

            poster_url = get_movie_poster_by_id(int(movie_id))

            result.append({
                "title": title,
                "rating": rating,
                "poster": poster_url
            })

        return jsonify({
            "recommendations": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == '__main__':

    app.run(debug=True)
