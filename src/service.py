import bentoml
import pandas as pd
from pydantic import BaseModel
from starlette.responses import JSONResponse
from src.jwt_middleware import create_jwt_token, USERS



class InputModel(BaseModel):
    '''
    Input data model for university admission prediction:
    GRE Score,TOEFL Score,University Rating,SOP,LOR ,CGPA,Research
    '''
    gre_score: int
    toefl_score: int
    university_rating: int
    sop: float
    lor: float
    cgpa: float
    research: int

@bentoml.service
class UniversityAdmissionService:
    def __init__(self):
        self.model = bentoml.models.get('university_admission_rf_model:latest').load_model()

    @bentoml.api
    def login(self, credentials: dict) -> dict:
        username = credentials.get('username')
        password = credentials.get('password')
        if username in USERS and USERS[username] == password:
            token = create_jwt_token(username)
            return {'token': token}
        else:
            return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    @bentoml.api
    def predict(self, input_data: InputModel) -> dict:
        # Convert input to DataFrame with proper column names
        input_dict = {
            'GRE Score': [input_data.gre_score],
            'TOEFL Score': [input_data.toefl_score],
            'University Rating': [input_data.university_rating],
            'SOP': [input_data.sop],
            'LOR ': [input_data.lor],  # Note the space after LOR
            'CGPA': [input_data.cgpa],
            'Research': [input_data.research]
        }
        input_df = pd.DataFrame(input_dict)
        prediction = self.model.predict(input_df)
        return {'admission_chance': float(prediction[0])}