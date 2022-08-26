# Backend - Trivia API

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

## Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Run the Server

To run the application run the following commands while virtual env is activated:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": False,
    "error": 404,
    "message": "not found"
}
```

The API will return three error types when requests fail:

- 405: Method Not Allowed
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Sample: `curl http://127.0.0.1:5000/categories`
- Returns: An object with a key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/categories?page=1`
- Returns: An object with a list of question objects, object of categories, success value, current_category and total number of questions

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 5,
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
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
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
    }
  ],
  "success": true,
  "total_questions": 19
}
```

`DELETE '/questions/:question_id'`

- Deletes the question of the given ID if it exists
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`
- Returns: The id of the deleted question and a success value

```json
{
  "deleted": 2,
  "success": true
}
```

`POST '/questions'`

- Carries out a search if `searchTerm` is provided else it creates a new question if the payload is valid
- When `searchTerm` is provided

  - Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{ "searchTerm": "title" }'`
  - Returns: The current_category, a list questions that match the search, a success value and total number of questions

  ```json
  {
    "current_category": 4,
    "questions": [
      {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }
    ],
    "success": true,
    "total_questions": 2
  }
  ```

- When `searchTerm` is not provided and the payload is valid

  - Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{ "answer": "short wave length", "question": "The sky is blue because blue light has a _____", "category": 1, "difficulty": 2 }'`
  - Returns: The created question and a success value

  ```json
  {
    "question": {
      "answer": "short wave length",
      "category": 1,
      "difficulty": 2,
      "id": 25,
      "question": "The sky is blue because  blue light has a _____"
    },
    "success": true
  }
  ```

`GET '/categories/:category_id/questions'`

- Gets all the questions the given category ID
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
- Returns: The current category ID, a list of questions, a success value and total number of questions

```json
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "short wave length",
      "category": 1,
      "difficulty": 2,
      "id": 25,
      "question": "The sky is blue because  blue light has a _____"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

`POST '/quizzes'`

- Gets a random question from the DB. If category ID is given, it picks a question from that category and it doesn't pick questions that are part of the previous questions list. It returns null if no questions matches these criteria
- Sample: `curl -X POST http://127.0.0.1:5000/questions/2 -H "Content-Type: application/json" -d '{ "previous_questions": [20, 21, 25], "quiz_category": { "id": 1 } }'`
- Returns: A question and a success value

```json
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```

## Deployment N/A

## Authors

The good folks at Udacity and yours truly, Emmanuel Menyaga.

## Acknowledgements

The awesome team at Udacity, Coach Caryn and all of the students.
