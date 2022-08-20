# Trivia
Trivia is used as the final project in the second section of [Udacity full stack nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044?utm_campaign=12948014301_c_individuals_btlpromo&utm_campaign=12948014301_c_individuals&utm_keyword=udacity%20full%20stack_e&utm_keyword=udacity%20full%20stack_e&utm_medium=ads_r&utm_medium=ads_r&utm_source=gsem_brand&utm_source=gsem_brand&utm_term=127442641891&utm_term=127442641891).
The frontend is complete and students are required to finish the backend API and if students are willing, 
they can change the styles and add some other functionalities to the frontend.

---

## Guidelines
1. Follow the pep8 style guide
2. The naming convention for the functions in the [test_flaskr.py](./backend/test_flaskr.py) file in the backend folder is 
```
test_(error code if apllicable)_(method)_(function name from __init__.py in the flask app)

Example:
With error:
test_405_get_categories

Without error:
test_get_categories
```
The Flask([flaskr](./backend/flaskr)) app can be located in backend folder

---

## Prerequisites and installation
**Prerequisites**: *Nodejs* and *python* should have been installed

**Frontend Installation and Local Development**:
1. Navigate to the frontend folder
2. Run `npm install` to install all dependencies. This is run only once
2. Run `npm start`. Run this each time you want to start the sever

**Backend Installation and Local Developmetn**: If you choose don't need to use a virtual environment, skip options 2 and 3
1. Navigate to the backend folder
2. Create a virtual environment
```
On your command prompt or terminal run:
python3 -m pip install virtualenv   

python3 -m venv venv
```
3. Activate the virtual environment
```
Windows
venv\Scripts\activate.bat

Linux/Mac
source venv/bin/acivate
```
4. set the flask APP and DEBUG state
```
Windows
set FLASK_APP=flaskr
set FLASK_DEBUG=1

Linux/Mac
export FLASK_APP=flaskr
export FLASK_DEBUG=1
```
5. Run the flask app with `flask run`

---

## API Reference
Trivia API operations is fully based on RESTful API. The status code used in this API are conventional http response code

Base URL: http://127.0.0.1:5000 or http://localhost:5000

API KEYS: This project doesn't use any API keys since its only used locally

### **Error**
Errors that have been handled programmatically are: 400, 404, 405 and 422 and they are returned in the following json format
```
{
  "error": 422, 
  "message": "Unprocessable", 
  "success": false
}
```

The messages returned by each status code:

400: Bad Request

404: Resource not Found

405: Method not Allowed

422: Unprocessable


### **Endpoints:**

**GET /categories**
- **General**:
    - **Description**: Used to get all available categories
    - **Returns** success value and an object of categories id and type
- **Sample**: `curl http://localhost:5000/categories`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

**GET /questions**
- **General**:
    - **Description**: Used to get all available questions
    - **Optional parameter**: page(this defaults to 1)
    - **Returns** success value, categories, current_category,list of questions, total questions
- **Sample**: `curl http://localhost:5000/questions`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}
```
**DELETE /questions/{question_id}**
- **General**:
    - **Description**: Used to get delete a question
    - **Returns** success value
- **Sample**: `curl http://localhost:5000/questions/9 -X DELETE`
```
{
  "success": true
}
```
**POST /questions**
- **General**:
    - **Description**: Used to get all submit a new question
    - **Requires**: question, answer, category(type=integer), difficulty(type=integer)
    - **Returns** success value
- **Sample**: `curl -X POST http://127.0.0.1:5000/questions -H 'Content-type: application/json' -d '{"question": "What is my name?", "answer": "Ayomide", "difficulty": 2, "category": 2}'`                 
```
{
  "success": true
}
```
**POST /questions**
- **General**:
    - **Description**: Used to search for questions
    - **Requires**: searchTerm
    - **Returns** success value, list of questions
- **Sample**: `curl -X POST http://127.0.0.1:5000/questions -H 'Content-type: application/json' -d '{"searchTerm":"who"}'`
```
{
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true
}
```
**GET /categories/{category_id}/questions**
- **General**:
    - **Description**: Used to get all available questions of the same category
    - **Returns** success value and a list of questions
- **Sample**: `curl http://localhost:5000/categories/2/questions`
```{
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Ayomide", 
      "category": 2, 
      "difficulty": 2, 
      "id": 27, 
      "question": "What is my name?"
    }
  ], 
  "success": true
}
```
**POST /quizzes**
- **General**:
    - **Description**: Used to get new question for the quiz
    - **Requires**: quiz_category, previous_questions(This is a list of previous_questions id)
    - **Returns** success value, question
- **Sample**: `curl http://localhost:5000/quizzes -H 'Content-Type:application/json' -X Post -d '{"previous_questions":[21,17], "quiz_category":{"id":0, "type":"click"}}'`
```
{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }, 
  "success": true
}
```
# Authors
1. [Udacity](https://www.udacity.com)
2. [Ay-Source](https://github.com/Ay-source)

# Acknowledgements
- [ALX-T](https://www.alx-t.com/)
- [Udacity](https://www.udacity.com)