import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

file = r"D:\GridGuard\Codes\RealTime_GridDataset_500.xlsx"
df = pd.read_excel(file)

class_targets = ["Weather Risk Level"]
reg_targets = ["Time_To_Recovery_min", "Microgrid_Survival_hr", "Grid Stress Score", "AI Confidence (%)"]

for col in df.select_dtypes(include='object'):
    df[col] = LabelEncoder().fit_transform(df[col].astype(str))

X = df.drop(columns=class_targets + reg_targets + ["Fault ID", "Fault_Location"])
results = {}

for t in class_targets:
    y = df[t]
    n_classes = y.nunique()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    mdl = XGBClassifier(
        objective="multi:softmax" if n_classes > 2 else "binary:logistic",
        num_class=n_classes if n_classes > 2 else None,
        eval_metric="mlogloss" if n_classes > 2 else "logloss",
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        early_stopping_rounds=10
    )
    mdl.fit(X_tr, y_tr, eval_set=[(X_te, y_te)], verbose=False)
    results[t] = f"Accuracy: {accuracy_score(y_te, mdl.predict(X_te)):.2f}"

for t in reg_targets:
    y = df[t]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    mdl = XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="rmse",
        early_stopping_rounds=10
    )
    mdl.fit(X_tr, y_tr, eval_set=[(X_te, y_te)], verbose=False)
    results[t] = f"MSE: {mean_squared_error(y_te, mdl.predict(X_te)):.2f}"

print("\nModel Performance Summary:")
for target, score in results.items():
    print(f"- {target}: {score}")
