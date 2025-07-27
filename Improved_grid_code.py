import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE


df = pd.read_excel(r"D:\GridGuard\Codes\Weather_Grid_Data.xlsx")


df['Load_per_Voltage'] = df['Load_MW'] / df['Voltage_V']
df['Pressure_Deviation'] = df['Pressure_hPa'] - df['Pressure_hPa'].mean()


feature_cols = ['Wind_Speed_kmph', 'Rainfall_mm', 'Pressure_hPa',
                'Voltage_V', 'Load_MW', 'Past_Outages_Count',
                'Load_per_Voltage', 'Pressure_Deviation']

X = df[feature_cols]
y = df['Blackout_Risk']


smote = SMOTE(random_state=42)
X_balanced, y_balanced = smote.fit_resample(X, y)


X_train, X_test, y_train, y_test = train_test_split(
    X_balanced, y_balanced, test_size=0.2, random_state=42, stratify=y_balanced)


best_params = {
    'colsample_bytree': 0.8,
    'learning_rate': 0.05,
    'max_depth': 5,
    'n_estimators': 200,
    'subsample': 1.0
}

model = xgb.XGBClassifier(**best_params, use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

print("\n✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))
print("\n✅ Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


xgb.plot_importance(model, importance_type='gain')
plt.title("Feature Importance")
plt.tight_layout()
plt.show()


results = X_test.copy()
results['Actual'] = y_test.values
results['Predicted'] = y_pred
results.to_excel("Improved_Predictions.xlsx", index=False)
print("\n✅ Predictions saved to 'Improved_Predictions.xlsx'")
