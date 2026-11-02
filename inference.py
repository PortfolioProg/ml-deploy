import pandas as pd
import pickle
with open('models/best_model_forest.pkl', 'rb') as f:
  model = pickle.load(f)

# Новые данные
new_data = pd.DataFrame({
    'pclass': [3],
    'age': [200],
    'fare': [0]
})

# Предсказание
predictions = model.predict(new_data)

# Вывод результатов
#print(f'{new_data.pclass:}')
print(new_data.iloc[0])
print("Predicted Survival:", predictions)
