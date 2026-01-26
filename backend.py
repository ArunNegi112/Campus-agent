from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI, HTTPException
from google.api_core.exceptions import ResourceExhausted
from fastapi.responses import JSONResponse
from ai_models.response_model import final_response


app = FastAPI()


#UserInput
class UserInput(BaseModel):
    user_query: Annotated[str, Field(...,description="Write your query here",examples=['When do we have kriti batra class on monday?'])]



#create endpoint
@app.post("/query")
def generate_output(user_input: UserInput):
    try:
        response = final_response(user_input.user_query)
        return JSONResponse(status_code=200, content={"response": response})
    except ResourceExhausted as error:
        raise HTTPException(status_code=429,detail="RESOURCES EXHAUSTED, You have reached the token limit")
    except Exception as error:
        raise HTTPException(status_code=500, content={"error": str(error)})