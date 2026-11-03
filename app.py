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

@app.get('/')
def status():
    return {'Status': 'OK'}

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
    uvicorn.run(app, host='0.0.0.0', port=5000)