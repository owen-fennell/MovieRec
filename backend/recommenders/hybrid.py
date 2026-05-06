from recommenders.base import BaseRecommender
from recommenders.content_based import ContentBasedEngine
from recommenders.collaborative import CollaborativeEngine

ALPHA = 0.5

class HybridEngine(BaseRecommender):

    def __init__(self):
        super().__init__()
        self.cf_engine  = CollaborativeEngine()
        self.cbf_engine = ContentBasedEngine()

    def load(self):
        self.cf_engine.ensure_data_loaded()
        self.cbf_engine.ensure_data_loaded()

    def _normalize(self, scores: dict) -> dict:
        if not scores:
            return {}

        min_score   = min(scores.values())
        max_score   = max(scores.values())
        score_range = max_score - min_score

        if score_range == 0:
            return {movie_id: 0.0 for movie_id in scores}

        return {
            movie_id: (score - min_score) / score_range
            for movie_id, score in scores.items()
        }

    def _to_score_dict(self, recommendations: list) -> dict:
        return {r['movieId']: r['score'] for r in recommendations}

    def _blend_scores(self, cf_scores: dict, cbf_scores: dict) -> dict:
        cf_norm  = self._normalize(cf_scores)
        cbf_norm = self._normalize(cbf_scores)

        all_movie_ids = set(cf_norm) | set(cbf_norm)

        blended = {}
        for movie_id in all_movie_ids:
            cf_score  = cf_norm.get(movie_id, 0.0)
            cbf_score = cbf_norm.get(movie_id, 0.0)
            blended[movie_id] = ALPHA * cf_score + (1 - ALPHA) * cbf_score

        return blended

    def recommend(self, user_id, n=10):  
        self.ensure_data_loaded()        

        cf_recs  = self.cf_engine.recommend(user_id, n=100)
        cbf_recs = self.cbf_engine.recommend(user_id, n=100)

        if not cf_recs and not cbf_recs:
            return []
        if not cf_recs:
            return cbf_recs[:n]
        if not cbf_recs:
            return cf_recs[:n]

        cf_scores  = self._to_score_dict(cf_recs)
        cbf_scores = self._to_score_dict(cbf_recs)
        blended    = self._blend_scores(cf_scores, cbf_scores)

        top_movies = sorted(blended, key=blended.get, reverse=True)[:n]
        top_scores = [blended[m] for m in top_movies]

        return self.format_results(top_movies, top_scores)
