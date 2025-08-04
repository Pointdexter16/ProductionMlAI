from typing import Annotated,Literal
from pydantic import BaseModel,Field,field_validator,computed_field
from config.city import tier_1_cities,tier_2_cities
all_cities=set(tier_1_cities+tier_2_cities)

class Customer(BaseModel):
    age:Annotated[int,Field(...,discription="enter the age of the custormer",example=35)]
    weight:Annotated[float,Field(...,discription="enter the weight of the custormer in kg",example=75.4)]
    height:Annotated[float,Field(...,discription="enter the height of the custormer in meter",example=1.75)]
    income:Annotated[float,Field(...,discription="enter the income of the custormer in lpa",example=12)]
    smoker:Annotated[int,Field(...,discription="enter the whether the the custormer smokes",example=0)]
    city:Annotated[str,Field(...,discription="enter the city of  the the custormer",example='delhi')]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
                                 'business_owner', 'unemployed', 'private_job'],
                                 Field(...,discription="enter the age of the custormer",example='government_job')]


    @field_validator('city')
    @classmethod
    def cityCheck(cls,value):
        value = value.title()
        if value not in all_cities:
            raise ValueError("given city not supported")
        return value.title()

    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3