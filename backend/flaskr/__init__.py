import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, close, rollback

QUESTIONS_PER_PAGE = 10

def all_categories():
    """Gets all categories along with their ids from database."""
    categories = Category.query.order_by(Category.id).all()
    categories = {
        category.id: category.type for category in categories
        }

    return categories

def list_categorized_questions(category_id):
    """Get questions with the same category from the database"""
    try:
        if category_id == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == category_id).all()
        questions = [question for question in questions]

        return [question.format() for question in questions]
    except:
        abort(422)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)


    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        return jsonify({
            "success": True,
            "categories": all_categories()
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        #Gets page number and database contents
        page = request.args.get("page", 1, type=int)
        questions = Question.query.order_by(Question.id).all()
        questions = [question.format() for question in questions]
        
        #Handles pagination
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        #Checks if requested page exists
        if questions[start:end] == []:
            abort(404)

        #List of categories to be returned
        questions_returned = questions[start:end]
        current_category = [i["category"] for i in questions_returned]

        return jsonify({
            "success": True,
            "questions": questions[start:end],
            "total_questions": len(questions),
            "categories": all_categories(),
            #Adviced by Udacity reviewer to return a list of categories instead of None
            "current_category": current_category
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).\
            one_or_none()
        
        #If question to be deleted doesn't exists in the database
        if question is None:
            abort(422)
        
        try:
            question.delete()
            close()
        except:
            rollback()
            close()
            abort(400)
        return jsonify({
            "success": True,
            "id": question_id
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def post_question():
        #check id each value in checks is in the form submitted and are not empty
        checks = ["question", "answer", "category", "difficulty"]
        body = request.get_json()
        if "searchTerm" in body:
            return search_questions()
        for check in checks:
            if check not in body or not body[check]:
                abort(400)

        #Adds new row to the database
        try:
            new_question = Question(
                question=body.get("question"), 
                answer=body.get("answer"), 
                category=body.get("category"), 
                difficulty=body.get("difficulty")
            )
            new_question.insert()
            close()
        except:
            rollback()
            close()
            abort(422)

        return jsonify({
            "success": True,
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions", methods=["POST"])
    def search_questions(body=''):
        #Searches for similar terms in the database
        body = request.get_json()
        if "searchTerm" not in body:
            return post_question()
        if len(body) > 1:
            abort(400)
        search_term = body.get("searchTerm")

        items = Question.query.order_by(Question.id).\
            filter(Question.question.ilike(f"%{search_term}%"))
        items = [item.format() for item in items]
        
        return jsonify({
            "success": True,
            "questions": items
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def categorized_questions(category_id):
        return jsonify({
            "success": True,
            "questions": list_categorized_questions(category_id)
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def quizzes():
        body = request.get_json()

        try:
            #Check if parameters exists
            checks = ["quiz_category", "previous_questions"]
            for check in checks:
                if check not in body:
                    abort(400)
            category_id = body["quiz_category"]["id"]
            previous_questions = body["previous_questions"]

            #Getting available questions
            questions = list_categorized_questions(category_id)
            if questions == []:
                abort(422)
            available_questions = [question["id"] for question in questions]
            if previous_questions:
                for i in previous_questions:
                    available_questions.remove(i)
            
            if available_questions:
                #Pick a random available question
                rand = random.choice(available_questions)

                #Gets a new question for the client
                for question in questions:
                    if question["id"] == rand:
                        new_question = question
                        break
            else:
                new_question = ''
        except Exception as e:
            print(e)
            abort(422)
        
        print("same here")
        return jsonify({
            "success": True,
            "question": new_question
        })



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not Allowed"
        }), 405

    @app.errorhandler(404)
    def resource_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def Unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app

