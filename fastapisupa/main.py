# Fastapi imports
from fastapi import FastAPI,HTTPException

# Supabase imports
from supabase import create_client, Client

# Openai imports
import openai

# Other imports 
from decouple import config
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

## Gemini api
import google.generativeai as genai


## intiate fastapi instance 
app=FastAPI()

## Supabase Configuration
SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_KEY = config('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

## Open AI Configuration
openai.api_key = config('OPENAI_API_KEY')
 
## Gemini 
GOOGLE_API_KEY=config('GEMINI_API_KEY')


# Models
class Character(BaseModel):
    id: Optional[UUID] = None
    number: Optional[int] = None
    name: str
    details: str


                                    ## APIs ##

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


## List all Characters
@app.get('/api/list_characters/',response_model=List[Character])
def list_users():
    response = supabase.table("characters").select("*").execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="No character list found")
    return response.data


## Generate  short story ##
@app.post('/api/generate_story/{user_id}')
def generate_story(user_id:UUID):
    response = supabase.table("characters").select("*").eq("id", str(user_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Character not found")
    character = response.data[0]

    ## Generate a story
    prompt = f"Write a five sentence short story about the following character:\n\nName: {character['name']}\nDetails: {character['details']}\n"
    
    ## Using OpenAi (commented because of its not free)
    # try:
    #     openai_response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a creative story writer."},
    #             {"role": "user", "content": prompt}
    #         ],
    #         max_tokens=150
    #     )
    #     story = openai_response.choices[0].message['content'].strip()
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f"Failed to generate story: {str(e)}")


    ## Using Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        story=response.text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate story: {str(e)}")

    return {"story": story}



## server setup
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)