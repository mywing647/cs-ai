import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data_path = r"data\data.csv"
try:
    df = pd.read_csv(data_path)
except Exception as e:
    print(e)
    exit()

df = df.dropna()
X = df.drop(columns = ["is_pro","player_name"])
y = df["is_pro"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = RandomForestClassifier(n_estimators=100, random_state=1)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"accuracy: {accuracy*100:.2f}%")

feature_importances = pd.DataFrame({
    'name': X.columns,
    'weight': model.feature_importances_
}).sort_values(by='weight', ascending=False)

feature_importances['weight'] = (feature_importances['weight']*100).round(2)
print(feature_importances.to_string(index=False))