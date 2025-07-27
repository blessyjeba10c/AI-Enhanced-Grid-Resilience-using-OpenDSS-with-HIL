import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
data = pd.read_csv(r"D:\GridGuard\Codes\grid_data.csv", encoding='ISO-8859-1')
X = data[['Voltage', 'Current', 'Frequency', 'Weather']]
y = data['Fault']
X = X.copy()
X['Weather'] = X['Weather'].astype('category').cat.codes
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
print("✅ Model trained successfully!")
print(f"📊 Accuracy: {accuracy*100:.2f}%")
print("🧮 Confusion Matrix:")
print(conf_matrix)
sample_data = pd.DataFrame({
    'Voltage': [230],
    'Current': [5.2],
    'Frequency': [50.0],
    'Weather': [0]
})
prediction = model.predict(sample_data)
print("🔍 Fault Predicted for new data:", prediction)
