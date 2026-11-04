import pandas as pd
import pickle
with open('models/best_model_forest.pkl', 'rb') as f:
  model = pickle.load(f)

# Новые данные
df = pd.DataFrame({
    'pclass': [1],
    'age': [5],
    'fare': [50]
})

# Предсказание
predictions = model.predict(df)

# Вывод результатов
print(df.iloc[0])
print("Predicted Survival:", predictions)

