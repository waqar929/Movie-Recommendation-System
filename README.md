# 🎬 Movie Recommendation System

A Hybrid Movie Recommendation System built using **SVD (Singular Value Decomposition)** and **Content-Based Filtering** techniques. The system recommends movies based on user preferences and movie similarities.

## 🚀 Features

- Movie Recommendations
- Collaborative Filtering using SVD
- Content-Based Filtering
- Cosine Similarity for Similar Movies
- User-Friendly Web Interface
- Fast and Accurate Recommendations

## 🛠️ Technologies Used

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Surprise (SVD)
- HTML/CSS

## 📂 Project Structure

movie-recommendation-system/
│
├── demo.py
├── dataset/
│   └── movies.csv
├── model/
│   └── svd_model.pkl
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
├── README.md
└── .gitignore

## ⚙️ Installation

### 1. Clone Repository

git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run Application

python app.py

### 4. Open Browser

http://127.0.0.1:5000

## 🧠 How It Works

### Collaborative Filtering (SVD)

The SVD model learns user preferences from movie ratings and predicts ratings for unseen movies.

### Content-Based Filtering

Movies are recommended based on similarity between movie features such as genres, keywords, and descriptions.

### Hybrid Recommendation

The final recommendation combines:
- SVD Predictions
- Content Similarity Scores

## 📊 Dataset

This project uses the MovieLens dataset for training and evaluation.

## 🎯 Future Improvements

- Deep Learning Based Recommendations
- TMDB API Integration
- Movie Posters
- User Authentication
- Real-Time Recommendations

## 🤝 Contributing

Contributions are welcome.

## 📜 License

Educational and learning purposes.

## 👨‍💻 Author

Waqar Ali
