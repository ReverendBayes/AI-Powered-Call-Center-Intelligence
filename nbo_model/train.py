import pandas as pd
from joblib import load, dump
from sklearn.pipeline import Pipeline
import xgboost as xgb

def main():
    # 1. Load customer features and offer uptake
    features = pd.read_csv('data/raw/churn-in-telecom-dataset.csv')
    uptake = pd.read_csv('data/raw/offer_uptake.csv')  # must have customer_id, offer_id
    # 2. Merge on customer_id
    df = features.merge(uptake, on='customer_id')
    # 3. Load churn artifacts
    preprocessor = load('churn_model/artifacts/churn_preprocessor.joblib')
    churn_model = load('churn_model/artifacts/churn_model.joblib')
    # 4. Compute churn probability
    X_all = features.drop(columns=['churn', 'phone number'])
    churn_prob = churn_model.predict_proba(preprocessor.transform(X_all))[:, 1]
    df['churn_prob'] = churn_prob[df.index]
    # 5. Features for NBO (reuse same preprocessor + churn_prob)
    X = df.drop(columns=['customer_id', 'offer_id', 'churn', 'phone number'])
    # 6. Train one binary model per offer
    offers = df['offer_id'].unique()
    for offer in offers:
        y = (df['offer_id'] == offer).astype(int)
        pipe = Pipeline([
            ('prep', preprocessor),
            ('clf', xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss'))
        ])
        pipe.fit(X, y)
        dump(pipe, f'nbo_model/artifacts/{offer}.joblib')
        print(f'Trained and saved model for offer: {offer}')

if __name__ == '__main__':
    main()
