import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load Data
df = pd.read_csv('Model Data.csv')

# Remove first row if it's national aggregate (India row)
df = df[df["India/ State/UT"] != "India"]

# Features and Targets
features = ['Projector %', 'Smart Class facility %', 'Digital Library %',
            'Computer Facility %', 'Internet Facility %', 'Library/ Reading Corner %',
            'Playground %', "Functional Girls' Toilet%", "Functional Boys' Toilet %",
            'Functional Electricity %', 'Functional Drinking Water %', 'Hand wash facility %']

X = df[features].astype(float)
y_promotion = df['Promotion Rate'].astype(float)
y_dropout = df['Dropout Rate'].astype(float)

# Train-Test Split
X_train, X_test, y_train_prom, y_test_prom = train_test_split(X, y_promotion, test_size=0.2, random_state=42)
_, _, y_train_drop, y_test_drop = train_test_split(X, y_dropout, test_size=0.2, random_state=42)

# Train Models
prom_model = RandomForestRegressor(random_state=42)
drop_model = RandomForestRegressor(random_state=42)

prom_model.fit(X_train, y_train_prom)
drop_model.fit(X_train, y_train_drop)

# Save the models
with open('prom_model.pkl', 'wb') as f1:
    pickle.dump(prom_model, f1)

with open('drop_model.pkl', 'wb') as f2:
    pickle.dump(drop_model, f2)

print("Models trained and saved successfully!")
