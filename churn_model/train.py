import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score
from joblib import dump

# Features to group using Sturges' formula (largest value per column)
GROUP_FEATURES = [
    'number vmail messages', 'total day minutes', 'total day calls', 'total day charge',
    'total eve minutes', 'total eve calls', 'total eve charge',
    'total night minutes', 'total night calls', 'total night charge',
    'total intl minutes', 'total intl calls'
]
# Original columns to use (excluding phone number)
BASE_FEATURES = [
    'state', 'account length', 'area code', 'international plan', 'voice mail plan',
    'number vmail messages', 'total day minutes', 'total day calls', 'total day charge',
    'total eve minutes', 'total eve calls', 'total eve charge',
    'total night minutes', 'total night calls', 'total night charge',
    'total intl minutes', 'total intl calls', 'total intl charge',
    'customer service calls'
]

# Weights for soft voting
VOTE_WEIGHTS = {'lr': 0.4, 'dt': 0.3, 'nb': 0.3}


def compute_bins(n_max: float) -> int:
    """
    Sturges' formula: K = 1 + log2(n_max)
    """
    return int(np.floor(1 + np.log2(max(1, n_max))))


def main():
    # Ensure artifacts directory exists
    os.makedirs('churn_model/artifacts', exist_ok=True)

    # 1. Load and group features
    df = pd.read_csv('data/raw/churn-in-telecom-dataset.csv')
    for feat in GROUP_FEATURES:
        max_val = df[feat].max()
        K = compute_bins(max_val)
        disc = KBinsDiscretizer(n_bins=K, encode='ordinal', strategy='uniform')
        df[f'{feat}_group'] = disc.fit_transform(df[[feat]]).astype(int)

    # 2. Prepare feature matrix X and target y
    all_feats = BASE_FEATURES + [f'{f}_group' for f in GROUP_FEATURES]
    X = df[all_feats]
    y = df['churn'].astype(int)

    # 3. Split 80/20 train/test stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # 4. Preprocess: one-hot encode categorical columns
    cat_cols = ['state', 'international plan', 'voice mail plan']
    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
        ('num', 'passthrough', [c for c in all_feats if c not in cat_cols])
    ])
    X_train_enc = preprocessor.fit_transform(X_train)
    X_test_enc = preprocessor.transform(X_test)

    # 5. Level 1: XGBoost
    xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_model.fit(X_train_enc, y_train)
    dump(preprocessor, 'churn_model/artifacts/preprocessor.joblib')
    dump(xgb_model, 'churn_model/artifacts/xgb_model.joblib')

    # 6. Generate Level-1 probabilities for train/test
    prob_train = xgb_model.predict_proba(X_train_enc)[:, 1].reshape(-1, 1)
    prob_test = xgb_model.predict_proba(X_test_enc)[:, 1].reshape(-1, 1)

    # 7. Prepare Level-2 training data
    X2_train = np.hstack([X_train_enc, prob_train])
    X2_test = np.hstack([X_test_enc, prob_test])

    # 8. Level 2: train LR, DT, NB
    lr = LogisticRegression(max_iter=1000, random_state=42).fit(X2_train, y_train)
    dt = DecisionTreeClassifier(random_state=42).fit(X2_train, y_train)
    nb = GaussianNB().fit(X2_train, y_train)
    dump(lr, 'churn_model/artifacts/lr_model.joblib')
    dump(dt, 'churn_model/artifacts/dt_model.joblib')
    dump(nb, 'churn_model/artifacts/nb_model.joblib')

    # 9. Soft voting on test set
    p_lr = lr.predict_proba(X2_test)[:, 1]
    p_dt = dt.predict_proba(X2_test)[:, 1]
    p_nb = nb.predict_proba(X2_test)[:, 1]
    final_prob = VOTE_WEIGHTS['lr'] * p_lr + \
                 VOTE_WEIGHTS['dt'] * p_dt + \
                 VOTE_WEIGHTS['nb'] * p_nb
    y_pred = (final_prob >= 0.5).astype(int)

    # 10. Evaluate
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"AUC:       {roc_auc_score(y_test, final_prob):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")


if __name__ == '__main__':
    main()