class NBOFactory:
    def __init__(self, builders):
        self.builders = builders

    def recommend(self, df, churn_prob):
        df = df.copy()
        df['churn_prob'] = churn_prob
        scores = {k: pipe.predict_proba(df)[:, 1] for k, pipe in self.builders.items()}
        best = max(scores, key=scores.get)
        return best, scores[best]
