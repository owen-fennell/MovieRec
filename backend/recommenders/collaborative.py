import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from recommenders.base import BaseRecommender

class CollaborativeEngine(BaseRecommender):

    def __init__(self):
        super().__init__()
        self.user_item_matrix = None
        self.user_similarity = None
    
    def load(self):
        self.user_item_matrix = self._build_user_item_matrix()
        self.user_similarity = self._build_user_similarity()

    def _build_user_item_matrix(self):
        
        matrix = self.ratings_df.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        )
        return matrix
    
    def _build_user_similarity(self):
        
        filled = self.user_item_matrix.fillna(0)
        sim = cosine_similarity(filled)
        return pd.DataFrame(
            sim, 
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )
    

    def _get_similar_users(self, user_id, k=20):

        if user_id not in self.user_similarity.index:
            return []
        
        similar = (
            self.user_similarity[user_id]
            .drop(user_id)  #remove the user themselves
            .dropna()       #remove any NaN similarities
            .nlargest(k)    #top k most similar users
        )
        return similar
    

    def _score_movies(self, user_id, similar_users):
        user_ratings = self.user_item_matrix.loc[user_id]
        unseen_movies = user_ratings[user_ratings.isna()].index

        scores = {}
        for movie_id in unseen_movies:
            neighbor_ratings = self.user_item_matrix.loc[
                similar_users.index, movie_id
            ].dropna()

            # Skip if none of the neighbors have rated this movie
            if neighbor_ratings.empty:
                continue

            # Weight each neighbor's rating by their similarity to our user
            weights = similar_users[neighbor_ratings.index]

            # Weighted average = sum(similarity * rating) / sum(similarities)
            scores[movie_id] = np.dot(neighbor_ratings, weights) / weights.sum()

        return scores
    
    def recommend(self, user_id, n=10):
        self.ensure_data_loaded()  # from BaseRecommender

        # Check this user exists in our matrix
        if user_id not in self.user_item_matrix.index:
            return []

        similar_users = self._get_similar_users(user_id)
        if len(similar_users) == 0:
            return []

        scores = self._score_movies(user_id, similar_users)
        if not scores:
            return []

        # Sort by score descending, take top n
        top_movies = sorted(scores, key=scores.get, reverse=True)[:n]
        top_scores = [scores[m] for m in top_movies]

        return self.format_results(top_movies, top_scores)