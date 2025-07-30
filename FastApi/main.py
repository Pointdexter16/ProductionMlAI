from fastapi import FastAPI,Path,HTTPException,Query
import json

app=FastAPI()

def data_load(name=None,id=None):
    with open("patients.json",'r') as f:
        data=json.load(f)
    return data


@app.get("/")
def hello():
    return {"message":"api to manage patients data using fastapi"}

@app.get("/view")
def view():
    return data_load()

@app.get("/patients/{id}")
def view_patient(id: str=Path(...,description="Enter the id which is in the DB",example='1')):
    data = data_load()
    for dataPoint in data:
        if dataPoint['id']==int(id):
            return dataPoint
    raise HTTPException(status_code=404,detail='Patient not found')


@app.get("/sort")
def sort(sort_by: str=Query(...,description='pass using which parameter you wanna sort \
                            like height_cm,weight_kg,bmi'),order:str=Query('asc',descriptio='how you wanna \
                                                                          sort it asc or desc')):
    valid_sort_by_opt=['height_cm','weight_kg','bmi']
    if sort_by not in valid_sort_by_opt:
        raise HTTPException(status_code=400,detail='Invalid field for sort by')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid field for sort order')
    
    data=data_load()
    reverse_opt=False if order=='asc' else True

    return sorted(data,key=lambda x: x.get(sort_by,0),reverse=reverse_opt)
