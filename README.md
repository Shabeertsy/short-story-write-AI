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

curl -X POST "http://127.0.0.1:8000/api/create_character/" -H "Content-Type: application/json" -d '{"name": "tony", "details": "tony is a rich man lives in usa"}'
response:- {"id":"1e80071d-7f50-40ad-8b80-f9d9634594ef","number":5,"name":"tony","details":"tony is a rich man lives in usa"}



curl -X 'GET'   'http://127.0.0.1:8000/api/list_characters/'   -H 'accept: application/json'
response:- [{"id":"34efb4fd-09e8-42ef-b9dc-ddcc8b55487c","number":2,"name":"string","details":"string"},{"id":"fe647e4d-3920-4f4a-8ecf-43330280655e","number":3,"name":"string","details":"string"},{"id":"7b27eeb2-56a9-4627-a7bd-8a2cc8227028","number":1,"name":"tom and jerry","details":"tom is a cat and jerry is a cat\n"},{"id":"daac0583-663d-45fc-b431-0ec8f139c14b","number":4,"name":"Bilbo Baggins","details":"Hobbit lives in the Shire owning a magic ring"},{"id":"1e80071d-7f50-40ad-8b80-f9d9634594ef","number":5,"name":"tony","details":"tony is a rich man lives in usa"}]



curl -X 'POST' \
  'http://127.0.0.1:8000/api/generate_story/daac0583-663d-45fc-b431-0ec8f139c14b' \
  -H 'accept: application/json' \
  -d ''
  
response:- {"story":"Bilbo Baggins, a peculiar hobbit residing in the serene Shire, cautiously kept a precious ring hidden within his humble abode. Its enchantment had the power to vanish the bearer from sight, a secret Bilbo guarded closely. As the day arrived for him to embark on an extraordinary adventure, he slipped the ring onto his finger, his eyes sparkling with both trepidation and a profound sense of destiny."}
