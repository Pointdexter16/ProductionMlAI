from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional

class Patient(BaseModel):

    patient_id:Annotated[str,Field(...,description='enter patient id',example='1')]
    name:Annotated[str,Field(...,description='enter patient id')]
    age:Annotated[int,Field(...,gt=0,description='enter age')]
    gender:str
    height_cm:Annotated[float,Field(...,gt=0,description='enter weight')]
    weight_kg:Annotated[float,Field(...,gt=0,description='enter weight')]
    blood_pressure:str
    heart_rate:int

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight_kg/((self.height_cm/100)**2),2)
    

class PatientUpdate(BaseModel):

    patient_id:Annotated[str,Field(...,description='enter patient id',example='1')]
    name:Annotated[Optional[str],Field(description='enter patient id',default=None)]
    age:Annotated[Optional[int],Field(gt=0,description='enter age',default=None)]
    gender:Optional[str]=None
    weight_kg:Annotated[Optional[float],Field(gt=0,description='enter weight',default=None)]
    height_cm:Annotated[Optional[float],Field(gt=0,description='enter weight',default=None)]
    blood_pressure:Optional[str]=None
    heart_rate:Optional[int]=None

app=FastAPI()

def data_load():
    with open("patients.json",'r') as f:
        data=json.load(f)
    return data

def saveData(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


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

@app.post("/create")
def create_patient(patient: Patient):

    data=data_load()

    if patient.patient_id in data:
        raise HTTPException(status_code=400,detail='patient already exists')
    
    data[patient.patient_id]=patient.model_dump(exclude=['patient_id'])

    saveData(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put("/update")
def create_patient(patient: PatientUpdate):

    data=data_load()

    if patient.patient_id not in data:
        raise HTTPException(status_code=400,detail="patient doesn't exists")
    
    dataPoint=data[patient.patient_id]
    patient_dic=patient.model_dump(exclude_unset=True)
    for field in patient_dic:
        dataPoint[field]=patient_dic[field]
    
    dataPoint['patient_id']=patient.patient_id

    updatedP=Patient(**dataPoint)

    data[patient.patient_id]=updatedP.model_dump(exclude=['patient_id'])

    saveData(data)

    return JSONResponse(status_code=200, content={'message':'patient updated successfully'})

@app.delete('/delete/{patientId}')
def deleteId(patientId):
    data = data_load()

    try:
        del data[patientId]
    except:
        raise HTTPException(status_code=400,detail='patient already exists')
    
    saveData(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})