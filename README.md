# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API Documentation

### Expected endpoints and behaviors

---

URI: `GET '/api/v1/categories'`

- Retrieves a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A JSON object with keys, categories, that contains an object of id: category_string key:value pairs and appropriate HTTP status code and success boolean.

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
  "success": true,
  "status_code": 200
}
```

---

URI: `GET '/api/v1/questions?page=${integer}'`

- Retrieves a set of questions, the total number of questions, all categories, the current category string and a success boolean.
- Request Arguments: `page` of type `integer`
- Returns: A JSON object with 10 paginated questions, total questions, object including all categories, current category string, and success boolean

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
  "current_category": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
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

---

URI: `GET '/api/categories/${id}/questions'`

- Retrieves questions for a given cateogry specified by an id request argument
- Request Arguments: `id` of type `integer`
- Returns: A JSON object with questions for the specified category, total questions, and current category string

```json
{
  "current_category": "Science",
  "questions": [
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
    }
  ],
  "success": true,
  "total_questions": 2
}
```

---

URI: `DELETE '/api/v1/questions/${id}'`

- Deletes a specified question resource by a given valid using question id
- Request Arguments: `id` of type `integer`
- Returns: A JSON object with the appropriate HTTP status code and success boolean. 

```json
{
  "status_code": 200,
  "success": true
}
```

---

URI: `POST '/api/v1/quizzes'`

- Sends a post request to retrieve a new, next question for the quizz game
Request Body:

```json
{
    "previous_questions": [5, 4, 10, 11],
    "quiz_category": {"type": "click", "id": 4}
}
```

- Returns: A JSON object with single, new, question object and success boolean.

```json
{
  "question": {
    "id": 12,
    "question": "Who invented Peanut Butter?",
    "answer": "George Washington Carver",
    "difficulty": 2,
    "category": 4
  },
  "success": true
}
```

---

URI: `POST '/api/v1/questions'`

- Sends a post request in order to create a new question resource
Request Body:

```json
{
  "question": "What is the largest lake in Africa?",
  "answer": "Lake Victoria",
  "difficulty": 2,
  "category": 3
}
```

- Returns: A JSON object with the appropriate HTTP status code and success boolean. 

```json
{
  "status_code": 200,
  "success": true
}
```

---

URI: `POST '/api/v1/questions'`

- Sends a post request in to search for a specific question or set of questions by a given search term
Request Body:

```json
{
  "searchTerm": "title"
}
```

- Returns: A JSON object with an array of questions, the number of totalQuestions that met the search term, the current category string, and success boolean.

```json
{
  "questions": [
    {
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "difficulty": 2,
      "category": 4
    }
  ],
  "totalQuestions": 1,
  "currentCategory": "Entertainment",
  "success": true
}
```

