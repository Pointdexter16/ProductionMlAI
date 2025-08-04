from typing import Annotated,Dict
from pydantic import BaseModel,Field

class Response(BaseModel):

    predicted_category:Annotated[str,Field(...,description='class predicted by the model',example='high')]
    confidence:Annotated[float,Field(...,description='confidence on the predicted class ranges from 0 to 1',example=0.76)]
    class_probabilities:Annotated[Dict[str,float],Field(...,description='classes and there confidences', example={"Low": 0.01, "Medium": 0.15, "High": 0.84})]

