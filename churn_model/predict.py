# churn_model/predict.py
# Uses the original 95% stacking model artifacts for churn prediction
import __main__
import joblib
import pandas as pd

# Expose to_dense into __mp_main__ so unpickling works when Joblib spawns subprocesses
def to_dense(X):
    return X.toarray()
__main__.to_dense = to_dense

class ChurnService:
    """
    Load the preprocessor and stacking classifier from the original 95% accurate pipeline.
    """
    def __init__(self,
                 preprocessor_path: str = 'churn_model/artifacts/churn_preprocessor.joblib',
                 model_path: str = 'churn_model/artifacts/churn_model.joblib'):
        # Load the preprocessor and stacking model artifacts
        self.preprocessor = joblib.load(preprocessor_path)
        self.model = joblib.load(model_path)

    def predict(self, df: pd.DataFrame) -> pd.Series:
        """
        Predict churn probability for each row in df.

        Parameters:
            df: pd.DataFrame with the same feature columns used in training (numerics and one-hot cats).

        Returns:
            pd.Series of churn probabilities (float between 0 and 1).
        """
        # Transform raw features to model-ready features
        X_proc = self.preprocessor.transform(df)
        # Predict probability for the positive class (churn=1)
        proba = self.model.predict_proba(X_proc)[:, 1]
        return pd.Series(proba, index=df.index)