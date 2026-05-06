import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from recommenders.base import BaseRecommender

# Define the genre columns
genre_cols = [
    'unknown', 'Action', 'Adventure', 'Animation', "Childrens",
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
    'FilmNoir', 'Horror', 'Musical', 'Mystery', 'Romance',
    'Sci-Fi', 'Thriller', 'War', 'Western'
] 

# Class created from inherited BaseRecommender
class ContentBasedEngine(BaseRecommender):

    # Initialize the content-based recommender
    def __init__(self):
        super().__init__()
        self.movie_vectors = None

    # Load the movie vectors
    def load(self):
        self.movie_vectors = self._build_movie_vectors()

    # Helper method to build the movie vectors based on the genre columns
    def _build_movie_vectors(self):
        return self.movies_df[genre_cols].values.astype(float)
    
    # Helper method to build the user vector based on the user's ratings
    def _build_user_vector(self, user_id: int):

        user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]

        if user_ratings.empty:
            return None
        
        id_to_index = {mid: i for i, mid in enumerate(self.movies_df['movieId'])}

        user_ratings = user_ratings[user_ratings['movieId'].isin(id_to_index)]

        indices = user_ratings['movieId'].map(id_to_index).values
        weights = user_ratings['rating'].values

        weighted_sum = np.dot(weights, self.movie_vectors[indices])
        return weighted_sum / weights.sum()
    
    def recommend(self, user_id, n=10):
        
        self.ensure_data_loaded()

        user_profile = self._build_user_vector(user_id)

        if user_profile is None:
            return []
        
        scores = cosine_similarity([user_profile], self.movie_vectors)[0]

        seen_ids = self.get_seen_ids(user_id)
        for movie_id in seen_ids:
            matches = self.movies_df[self.movies_df['movieId'] == movie_id].index
            if len(matches):
                scores[matches[0]] = 0
        
        top_indices = np.argsort(scores)[::-1][:n]

        top_ids = self.movies_df.iloc[top_indices]['movieId'].tolist()
        top_scores = scores[top_indices].tolist()

        return self.format_results(top_ids, top_scores)







