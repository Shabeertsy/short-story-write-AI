# Fastapi imports
from fastapi import FastAPI,HTTPException

# Supabase imports
from supabase import create_client, Client

# Other imports 
from decouple import config
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel


## intiate fastapi instance 
app=FastAPI()

# Supabase Configuration
SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_KEY = config('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Models
class Character(BaseModel):
    id: Optional[UUID] = None
    number: Optional[int] = None
    name: str
    details: str


## Apis ##

## create a character ##
@app.post('/api/create_character/',response_model=Character,status_code=201)
def create_character(character:Character):
    character.id=uuid4()

    ## get and update number ##
    response = supabase.table("characters").select("number").order("number", desc=True).limit(1).execute()
    if 'error' in response:
        raise HTTPException(status_code=400, detail=f"Failed to fetch characters: {response['error']}")
    max_number = response.data[0]['number'] if response.data else 0
    character.number = max_number + 1

    data = {"id": str(character.id), "number": character.number, "name": character.name, "details": character.details}
    try:
        response = supabase.table("characters").insert(data).execute()
        if 'error' in response:
            raise HTTPException(status_code=400, detail=f"Failed to create character: {response['error']}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    
    return character


## Generate  short story ##
@app.post('/api/generate_story/',response_model=Character,status_code=200)
def create_character(character:Character):
    character.id=uuid4()





## server setup
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)