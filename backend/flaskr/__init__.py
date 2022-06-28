from crypt import methods
from doctest import REPORT_NDIFF
import json
import os
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs [COMPLETED]
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories. [COMPLETED]
    """

    @app.route('/api/v1/categories', methods=['GET'])
    def retrieve_categories():
        # Handle request
        if request.method != 'GET':
            abort(405)

        # Handle data
        try:
            categories = db.session.query(Category).all()
            formatted_categories = {
                category.id: category.type for category in categories}
        except BaseException:
            abort(500)

        # Verify resource data
        if len(formatted_categories) == 0:
            abort(404)

        # Handle response
        return jsonify({
            'success': True,
            'status_code': 200,
            'categories': formatted_categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/api/v1/questions', methods=['GET'])
    def retrieve_questions():
        # Handle request
        if request.method != 'GET':
            abort(405)

        # Handle data
        try:
            questions = db.session.query(Question).order_by(Question.id).all()
            paginated_questions = paginate_questions(request, questions)
            response = retrieve_categories()
            data = json.loads(json.dumps(response.json))
        except BaseException:
            abort(500)

        # Verify resource data
        if len(paginated_questions) == 0:
            abort(404)

        # Handle response
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'categories': data.get('categories'),
            'current_category': 'Science',
        })

    def paginate_questions(request, questions):
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # Format data
        formatted_questions = [question.format() for question in questions]
        paginated_questions = formatted_questions[start:end]
        return paginated_questions

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_by_id(question_id):
        # Handle request
        if request.method != 'DELETE':
            abort(405)

            # Handle data
        question = db.session.query(Question).get_or_404(question_id)

        # Persist resource data
        try:
            db.session.delete(question)
            db.session.commit()
        except BaseException:
            abort(500)

            # Handle response
        return jsonify({
            'success': True,
            'status_code': 200
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score. [COMPLETED]

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at
    the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/api/v1/questions', methods=['POST'])
    def create_new_question():
        # Handle request
        if request.method != 'POST':
            abort(405)

        # Handle operation
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        if search_term:
            return retrieve_questions_by_search_term(search_term)

        # Validate request data
        if valid_question_format(body):
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)
        else:
            abort(400)

        # Handle data
        question_to_be_created = Question(
            question=new_question,
            answer=new_answer,
            difficulty=new_difficulty,
            category=new_category
        )

        # Persist resource data
        try:
            db.session.add(question_to_be_created)
            db.session.commit()
        except BaseException:
            abort(500)

        # Handle response
        return jsonify({
            'success': True,
            'status_code': 200
        })

    def valid_question_format(body):
        # Verify all required keys are present
        required_keys = ['question', 'answer', 'difficulty', 'category']
        is_present = all(key in body for key in required_keys)
        if not is_present:
            return False

        # Verify all keys have non zero or empty values
        has_values = all(body[key] for key in required_keys)
        return True if has_values else False

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question. [COMPLETED]

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    def retrieve_questions_by_search_term(search_term):
        # Handle data
        questions = (db.session
                     .query(Question)
                     .order_by(Question.id)
                     .filter(Question.question.ilike(f'%{search_term}%'))
                     .all())

        # Verify resource data
        if len(questions) == 0:
            abort(404)

        # Format data
        formatted_questions = [question.format() for question in questions]

        # Handle response
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': 'Entertainment'
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category. [COMPLETED]

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/api/v1/categories/<int:category_id>/questions',
               methods=['GET'])
    def retrieve_questions_by_category(category_id):
        # Handle request
        if request.method != 'GET':
            abort(405)

        # Verify valid category id
        category = db.session.query(Category).get_or_404(category_id)
        category_type = category.format()['type']

        # Handle data
        try:
            questions_by_category = (
                db.session
                .query(Question)
                .filter(Question.category == category_id)
                .all()
            )
            formatted_questions_by_category = [
                question.format()
                for question in questions_by_category
            ]
        except BaseException:
            abort(500)

            # Verify resource data
        total_questions_by_category = len(formatted_questions_by_category)
        if total_questions_by_category == 0:
            abort(404)

            # Handle response
        return jsonify({
            'success': True,
            'questions': formatted_questions_by_category,
            'total_questions': total_questions_by_category,
            'current_category': category_type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz. [COMPLETED]
    This endpoint should take category and previous question parameters
    and return a random question within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/v1/quizzes', methods=['POST'])
    def quiz_question():
        # Handle payload
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            category = body.get('quiz_category')
            category_type = category['type']
        except BaseException:
            abort(422)

        # Handle data
        next_question = None
        if category_type == 'click':
            all_questions = db.session.query(Question).all()

            if len(previous_questions) != len(all_questions):
                next_question = get_next_question(
                    previous_questions, all_questions)

                # Verify resource data
                if next_question['id'] in previous_questions:
                    abort(500)
        else:
            questions_by_category = (
                db.session .query(Question) .filter(
                    Question.category == category['id']) .all())

            if len(previous_questions) != len(questions_by_category):
                next_question = get_next_question(
                    previous_questions, questions_by_category)

                # Verify resource data
                if next_question['id'] in previous_questions:
                    abort(500)

        # Handle response
        return jsonify({
            'success': True,
            'question': next_question
        })

    def get_next_question(previous_questions, questions):
        formatted_questions = [question.format() for question in questions]
        next_questions = list(
            filter(lambda q: q['id']
                   not in previous_questions, formatted_questions)
        )
        return random.choice(next_questions)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422. [COMPLETED]
    """

    # --- App Request, Error Handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'requested resource not found'
        }), 404

    @app.errorhandler(405)
    def methhod_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unporcessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
