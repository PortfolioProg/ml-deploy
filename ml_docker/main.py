from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

with open('models/best_model_forest.pkl','rb') as f:
    model = pickle.load(f)

class PrInp(BaseModel):
    pclass: int
    age: int
    fare: float
    

app = FastAPI()

#curl http://127.0.0.1:5000

@app.get('/')
def status():
    return {'Status': 'OK'}

# curl -X POST http://localhost:5000/calc -H "Content-Type: application/json" -d '{"num":5}'

@app.post('/calc')
def calc(data: dict):
    return {'Result': data['num'] * 2}

# curl -X POST "http://127.0.0.1:5000/calc2?num=5&mul=2"

@app.post('/calc2')
def calc(num: int, mul: int):
    return {'Result': num * mul}

# curl -X POST http://localhost:5000/pred  -H "Content-Type: application/json"   -d '{"pclass": 2, "age": 2, "fare": 40}'

# curl -X POST http://ml.dazparts.com/pred  -H "Content-Type: application/json"   -d '{"pclass": 2, "age": 2, "fare": 40}'

@app.post('/pred')
def pred(data: PrInp):
    df = pd.DataFrame({
        'pclass': [data.pclass],
        'age': [data.age],
        'fare': [data.fare]
    })
    predicts = model.predict(df)
    result = 'Survived' if predicts[0]==1 else 'Not Survived'
    return {'prediction': result}
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=5000)