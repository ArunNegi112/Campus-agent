from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from ai_models.response_model import final_response


app = FastAPI()


#UserInput
class UserInput(BaseModel):
    user_query: Annotated[str, Field(...,description="Write your query here",examples=['When do we have kriti batra class on monday?'])]



#create endpoint
@app.post("/")
def generate_output(user_input: UserInput):
    try:
        response = final_response(user_input.user_query)
        return JSONResponse(status_code=200, content={"response": response})
    
    except HTTPException:
        raise

    except Exception as error:
        error_msg = str(error)
        error_type = type(error).__name__
        
        # Print full error for debugging
        print(f"Error Type: {error_type}")
        print(f"Error Message: {error_msg}")
        
        # Check if it's a rate limit/quota error
        if 'RESOURCE_EXHAUSTED' in error_msg:
            raise HTTPException(
                status_code=429,
                detail="API quota exceeded. Upgrade your API plan."
            )
        
        if error_type=="DefaultCredentialsError":
            raise HTTPException(
                status_code=429,
                detail="API quota exceeded, 'DefaultCredentialsError'"
            )