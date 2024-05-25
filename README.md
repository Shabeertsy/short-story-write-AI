Short Story writer using open ai

## users can add character and detials
## generate story  using character id or name

endpoints

api/create_character/
api/generate_story/
api/list_characters/

#installation
install requirements.txt

navigate to project folder  run using uvicorn main:app --reload


### curl command ##

curl -X POST "http://127.0.0.1:8000/api/create_character/" -H "Content-Type: application/json" -d '{"name": "robin", "details": "lives in a forest"}'

curl -X 'GET'   'http://127.0.0.1:8000/api/list_characters/'   -H 'accept: application/json'

curl -X 'POST' \
  'http://127.0.0.1:8000/api/generate_story/daac0583-663d-45fc-b431-0ec8f139c14b' \
  -H 'accept: application/json' \
  -d ''
