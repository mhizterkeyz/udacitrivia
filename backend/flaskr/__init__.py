from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_and_format_categories():
    categories = Category.query.order_by(Category.id).all()
    categories_map = {}
    for category in categories:
        formatted_category = category.format()
        categories_map[formatted_category['id']] = formatted_category['type']
    return categories_map

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    formatted_questions = [question.format() for question in selection]
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    return formatted_questions[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allo-Methods', 'GET, PUT, POST, DELETE, PATCH, OPTIONS')
        return response

    @app.route('/categories')
    def get_all_categories():
        return jsonify({
            'success': True,
            'categories': get_and_format_categories()
        })

    @app.route('/questions')
    def get_paginated_questions():
        selection = Question.query.order_by(Question.id, Question.id).all()
        questions = paginate_questions(request, selection)
        if not len(questions):
            return abort(404)
        
        return jsonify({
            'success': True,
            'questions': questions,
            'categories': get_and_format_categories(),
            'total_questions': len(selection),
            'current_category': questions[0]['category']
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            return abort(404)
        
        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            request_body = request.get_json()
            if 'searchTerm' in request_body:
                search_term = request_body['searchTerm']
                selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
                questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(selection),
                    'current_category': questions[0]['category'] if len(questions) else None
                })
            else:
                question = Question(**request_body)
                question.insert()

                return jsonify({
                    'success': True,
                    'question': question.format()
                }), 201
        except:
            return abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        selection = Question.query.filter(Question.category == category_id).all()
        questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            request_body = request.get_json()
            previous_questions = request_body['previous_questions']
            quiz_category = request_body['quiz_category']
            selection = Question.query.filter(~Question.id.in_(previous_questions))
            if 'id' in quiz_category:
                category_id = quiz_category['id']
                selection = selection.filter(Question.category == category_id)

            selection = selection.all()
            question = None
            if len(selection):
                question = random.choice(selection)

            return jsonify({
                'success': True,
                'question': question.format() if question else question
            })
        except:
            return abort(422)

    @app.errorhandler(422)
    def uprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app

