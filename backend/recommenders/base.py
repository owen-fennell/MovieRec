from abc import ABC, abstractmethod
import pandas as pd

class BaseRecommender(ABC):

    def __init__(self):
        self.movies_df = None
        self.ratings_df = None
        self.is_loaded = False

    def load_data(self):

        genre_cols = [
            'unknown', 'Action', 'Adventure', 'Animation', 'Childrens',
            'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
            'FilmNoir', 'Horror', 'Musical', 'Mystery', 'Romance',
            'Sci-Fi', 'Thriller', 'War', 'Western'
        ]
        self.movies_df = pd.read_csv(
            './data/ml-100k/u.item',
            sep='|',
            encoding='latin-1',
            header=None,
            names=['movieId', 'title', 'release_date', 'video_release',
                'imdb_url'] + genre_cols
        )
        self.movies_df = self.movies_df[['movieId', 'title'] + genre_cols]

        self.ratings_df = pd.read_csv(
            './data/ml-100k/u.data',
            sep='\t',
            header=None,
            names=['userId', 'movieId', 'rating', 'timestamp']
        )
        self.ratings_df = self.ratings_df.drop(columns='timestamp')

    @abstractmethod
    def load(self):

        pass


    @abstractmethod
    def recommend(self, user_id: int, num_recommendations: int = 10) -> list:

        pass

    def ensure_data_loaded(self):

        if not self.is_loaded:
            self.load_data()
            self.load()
            self.is_loaded = True

    def get_seen_ids(self, user_id: int) -> set:

        seen = self.ratings_df[self.ratings_df['userId'] == user_id]['movieId']
        return set(seen)
    
    def format_results(self, movie_ids: list, scores: list) -> list:
        
        results = []
        for movie_id, score in zip(movie_ids, scores):
            row = self.movies_df[self.movies_df['movieId'] == movie_id]
            if row.empty:
                continue
            results.append({
                'movieId': int(movie_id),
                'title': row.iloc[0]['title'],
                'score': round(float(score), 4)
            })
        return results