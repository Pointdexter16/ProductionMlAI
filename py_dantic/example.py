from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,computed_field
from typing import List,Dict,Optional,Annotated
class patient(BaseModel):
 
    name:str
    age: Annotated[int,Field(title='enter the age',description='enter the age of the patient it should be between 18 and 60',default=18)]
    weight: Annotated[float,Field(gt=0,strict=True)]
    height: Annotated[float,Field(gt=0)]
    email: EmailStr
    url: AnyUrl
    married:bool=False
    allergies: Annotated[Optional[List[str]],Field(max_length=5)]=None
    contact_details: Dict[str,str]

    @field_validator('email')
    @classmethod
    def checkEmail(cls,value):
        valid_values=['hdfc.com','icici.com']
        value=value.split('@')[-1]
        if value not in valid_values:
            raise ValueError('invalid email')
        return value

    @field_validator('name')
    @classmethod
    def upname(cls,value):
        return value.upper()

    @field_validator('age',mode='before')
    @classmethod
    def checkAge(cls,value):
        if (0<value<100)==0:
            raise ValueError("age not in acceptable range")
        return value
    
    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)

def insert_patient_data(Patient: patient):
    print(Patient.name)
    print(Patient.age)
    print(Patient.allergies)
    print(Patient.married)
    print(Patient.bmi)
    print('inserted')

patient_info={'name': 'shehzail','age':34,'weight':53.3, 
              'contact_details':{'email':'abbasshehzail123@gmail.com','phoneNo':'34234343'},
              'email':'abbasshehzail123@hdfc.com','url':"https://hello.com",'height':1.7}
Patient=patient(**patient_info)
insert_patient_data(Patient)


