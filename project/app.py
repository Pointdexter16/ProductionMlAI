from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.schema import Customer
from schema.response import Response
from model.model import model,model_prediction,MODEL_VERSION
import pandas as pd


app=FastAPI()


@app.get('/')
def home():
    return {'message':'home page to insurance evaluator'}

@app.get('/health')
def health():
    response={
        'api working':True,
        'model version':MODEL_VERSION,
        'model loaded':True if model else False
    }
    return response


@app.post('/predict',response_model=Response)
def predict(customer:Customer):

    input_df = pd.DataFrame([{
            'bmi': customer.bmi,
            'age_group': customer.age_group,
            'lifestyle_risk': customer.lifestyle_risk,
            'city_tier': customer.city_tier,
            'income_lpa': customer.income,
            'occupation': customer.occupation
        }])

    prediction = model_prediction(input_df)  
    return JSONResponse(status_code=200,content=prediction)