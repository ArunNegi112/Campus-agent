from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ai_models.response_model import final_response


app = FastAPI()


#UserInput
class UserInput(BaseModel):
    user_query = Annotated[str, Field(...,description="Write your query here",examples=['When do we have kriti batra class on monday?'])]



#create endpoint
@app.get("/query")
def generate_output(user_query: UserInput):
    try:
        response = final_response(user_query)
        return JSONResponse(status_code=200, content=response)
    except Exception as error:
        return JSONResponse(status_code=500,content=str(error))
    