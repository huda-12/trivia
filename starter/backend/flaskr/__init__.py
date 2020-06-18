import os
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import collections
from models import setup_db, Question, Category, db
from sqlalchemy import func
# above import all Dependencies (libraries)
QUESTIONS_PER_PAGE = 10  # how many question show per one page .
# it constant we can change if a different example
# pagination (every 10 questions)


def paginate_questions(request, selection):
    # helper method use to paginate questions
    # take parameter (request, selection)
    # passed parameter request and selection
    # Resource = lesson 3 part (error handling) BOOKSHELF EXAMPLE from UDACITY
    page = request.args.get('page', 1, type=int)
    # this to get number of page or 1 type integer
    start = (page - 1) * QUESTIONS_PER_PAGE
    # start pagination from (page stored -1) * 10
    end = start + QUESTIONS_PER_PAGE  # end pagination
    questions = [question.format() for question in selection]
    # format the questions
    current_questions = questions[start:end]
    # set current question in dictionary from start and end
    return current_questions  # return current question
    # Resource = lesson 3 part (error handling) BOOKSHELF EXAMPLE from UDACITY


def create_app(test_config=None):  # Method to craete app
    app = Flask(__name__)
    setup_db(app)  # setup app
    # @TODO: Set up CORS.
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # Cross-Origin Resource Sharing :allow website make request
    # form API which does not share same origin
    # here use CORS and pass parmeter app and object
    # resources to Resource Specific Usage
    # Resource = lesson 3 part (FLASK_CORS)

    @app.after_request  # flask app decorator and add some headers to response
    # Resource = lesson 3 part (FLASK_CORS) from UDACITY
    def after_request(response):
        # this method run after request pass response as parameter
        # take it and add some headers like Authorization and
        # method allowed then return response
        # Resource = lesson 3 part (FLASK_CORS) from UDACITY
        # List of http request header values the server will allow,
        # useful if you use any custom headers
        # Resource = lesson 3 part (CORS) from UDACITY
        # here Authorization
        # List of HTTP request types allowed here allowed to do
        # Resource = lesson 3 part (CORS) from UDACITY
        # PUT GET PATCH POST DELETE OPTIONS another method do not be allowed
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'PUT,GET,PATCH,POST,DELETE,OPTIONS')
        return response  # return response after add some headers
    # (GET categories)

    @app.route('/categories')
    # must Organizing API endpoints must be plural, noun ,not longer or complex
    # Resource = lesson 3 part (Organizing API endpoints) from UDACITY
    # here endpoint to handle GET requests all available categories.
    def get_categories():  # method to get all categories
        categories = Category.query.order_by(Category.type).all()
        # query to get Category table (stored in models.py from DB )
        # ordered by type of category and collect it all
        # Resource=lesson 3 part(error handling)BOOKSHELF EXAMPLE from UDACITY
        if len(categories) == 0:  # IF length categories is zero will
            # abort error type status code
            # 404 resource not found
            abort(404)
        return jsonify({  # if else will return jsonify contain success=true,
            # categories all available categories
            'success': True,
            'categories': {category.id: category.type
                           # create for loop category in categories
                           # to store dictionary contain
                           # [category.id: category.type]
                           # and store and render in categories
                           for category in categories}
                        })
    # Resource=lesson3 part(error handling)BOOKSHELF EXAMPLE from UDACITY
    # (GET questions)

    @app.route('/questions')
    # must Organizing API endpoints must be plural, noun ,not longer or complex
    # Resoure = form lesson 3 part (Organizing API endpoints)
    # here endpoint to handle GET requests all questions include pagination,
    # total questions ,categories,current category
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        # query to get Question table(stored in models.py from DB )
        # order by id of Questions and collect it all
        # Resource=lesson3 part(error handling)BOOKSHELF EXAMPLE from UDACITY
        formatted_questions = paginate_questions(request, questions)
        # use helper method paginate questions
        # written above and pass parameter request,
        # questions to start paginate
        # Resource=lesson3 part(error handling)BOOKSHELF EXAMPLE from UDACITY
        categories = Category.query.order_by(Category.type).all()
        # query to get Category table (stored in models.py from DB )
        # order by type of category and collect it all
        # Resource=lesson3 part(error handling)BOOKSHELF EXAMPLE from UDACITY
        if len(formatted_questions) == 0:
            # if page out of the range of questions = 0
            # will abort error type status code  404 resource not found
            abort(404)
            # Resource=lesson3 part(error handling)
            # BOOKSHELF EXAMPLE from UDACITY
            return jsonify({
                # and will be return jsonify success flag to False
                'success': False
                })
        return jsonify({
            # else if in the range and correct,
            # will be return jsonify contain success flag to True
            # questions stored paginate questions formated,
            # total_questions get all questions in DB,
            # and categories : store all categories
            # (create for loop category in categories
            # to store dictionary contain
            # [category.id: category.type] and store and render in categories)
            # current_category is none
            # Resource=lesson 3 part(error handling)
            # BOOKSHELF EXAMPLE from UDACITY
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': {category.id: category.type
                           for category in categories},
            'current_category': None
            })

    # (DELETE METHOD)
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    # must Organizing API endpoints must be plural, noun ,not longer or complex
    # with variable  name specifiecd integer
    # type name question_id to delete by id of questions
    # Resource = lesson 3 part (Organizing API endpoints) from UDACITY
    # here endpoint to handle DELETE questions specifiecd id of questions.
    # will be return jsonify success flag to sucess,
    # deleted : id of question Which is deleted
    def delete_questions(question_id):
        # define method name delete_questions and
        # pass parameter question_id
        # Resource=lesson 3 part(Flask Part II)AND(error handling)
        # BOOKSHELF EXAMPLE from UDACITY
        question = db.session.query(Question).get(question_id)
        # SQLALCHEMY library provide interact with myDB using session manges by
        # flask sqlalchemy and can acess session object as db
        # Session establishes and maintains all conversations and Transaction ,
        # here open session and query Question table to get
        # question_id for specific question
        # Resource=part1(SQL and Data Modeling for the Web)from UDACITY
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
        # AND https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
        if(question) is None:
            # if question is none will abort error
            # type status code 422 unprocessable
            abort(422)
        else:  # else it is not none
            try:
                question.delete()  # delete the question from db
            except SQLAlchemyError as e:  # catch any error sqlalchemy
                # Resource=https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy
                print(e)  # print errror
                db.session.rollback()  # call the rollback method
            finally:
                db.session.close()  # close the session
            return jsonify({
                "success": True,
                "deleted": question_id
                })

    # (POST method)
    @app.route('/questions', methods=['POST'])
    # must Organizing API endpoints must be plural, noun ,not longer or complex
    # Resource = lesson 3 part (Organizing API endpoints) from UDACITY
    # here endpoint to handle POST questions.
    # will be return jsonify success flag to sucess,
    # created : id of question Which is created
    # Resoure=from part 1 (SQL and Data Modeling for the Web) from UDACITY
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    # AND https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
    def create_question():
        # define method name create_question
        data = request.get_json()
        # get data from request json from frontend
        ques = data.get('question')
        # get question store in ques
        answer = data.get('answer')
        # get answer store in  answer
        difficulty = data.get('difficulty')
        # get difficulty store in difficulty
        category = data.get('category')
        # get category store in  category
        new_question = Question(  # new_question to store in  new Question
                       question=ques,
                       answer=answer,
                       category=category,
                       difficulty=difficulty
                        )
        new_question_id = new_question.id
        try:  # to check the session works well and catch the error
            new_question.insert()  # insert new quession to db
            new_question_id = new_question.id
        except Exception:  # catch error type status code 422 unprocessable
            abort(422)
            db.session.rollback()  # call the rollback method
        finally:
            db.session.close()  # close the session
        return jsonify({
            "success": True,
            "created": new_question_id
            })

    # (POST methods search)

    @app.route('/questions/search', methods=['POST'])
    # must Organizing API endpoints must be plural, noun ,not longer or complex
    # Resoure = form lesson 3 part (Organizing API endpoints) from UDACITY
    # here endpoint to handle POST search questions . will be return jsonify
    # success flag to sucess ,any questions for whom the search term ,
    # total_questions conatin search_term
    def search_question():
        # define method name search_question
        if (request.get_json().get('searchTerm') != ""):
            # check if search Term get from frontend is not empty
            # request to get json specific to get searchTerm from
            # frontend and stored in search_term
            search_term = request.get_json().get('searchTerm')
        if search_term:  # check search_term
            results = Question.query.filter(
                        # query all Question table and filter
                        # by question contain part of
                        # search_term or all(case insensitive)
                        Question.question.ilike(f'%{search_term}%')
                        # Resoure =
                        # https://stackoverflow.com/questions/20363836/postgresql-ilike-query-with-sqlalchemy
                        ).order_by(Question.id).all()
            # order query by Question.id and collect all to store in results
            return jsonify({
                'success': True,
                'questions': [question.format() for question in results],
                # for loop question in results and format question
                'total_questions': len(results),
                # length results mean how many questions contain search_term
                })
        abort(404)
        # else will abort error type status code  404 resource not found
    # (GET methods based on category.)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    # must Organizing API endpoints must be plural, noun ,not longer or complex
    # Resoure = form lesson 3 part (Organizing API endpoints) from UDACITY
    # here endpoint to handle GET questions based on category_idr.
    # will be return jsonify success flag to sucess,questions,current_category
    def get_questions_by_category(category_id):
        # define method name get_questions_by_category and
        # pass parameter category_id
        question = db.session.query(Question).get(question_id)
        # here open session and querry Question table to get
        # question_id for specific question
        try:  # to catch the error
            # query to get Category table(stored in models.py from DB)
            # filter by if Category.id==category_id(parameter)
            # and stored in category
            # Resoure=from lesson 3 part(error handling)
            # BOOK SHELF EXAMPLE from UDACITY
            category = Category.query.filter(
                       Category.id == category_id
                       ).one_or_none()
        # query to get Question table(stored in models.py from DB)
        # filter by if Question.category==category_id(parameter)
        # order by Question.id
        # collect all query and stored in questions
        # Resoure=from lesson 3 part(error handling)
        # BOOK SHELF EXAMPLE from UDACITY
            questions = Question.query.filter(
                        Question.category == category_id
                      ).order_by(Question.id).all()
            question = []  # open dictionary to question after format
            for q in questions:
                question.append(q.format())
                # Resoure =
                # https://www.w3schools.com/python/ref_list_append.asp
            return jsonify({
                'success': True,
                'questions': question,
                'total_questions': len(question),
                # length question which have same category
                'current_category': category.type
                })
        except Exception:
            # catch error type status code 404 resource not found
            abort(404)

    # (POST methods quizzes)
    @app.route('/quizzes', methods=['POST'])
    # must Organizing API endpoints must be plural, noun ,not longer or complex
    # Resoure = form lesson 3 part (Organizing API endpoints)
    # here endpoint to handle POST endpoint to get questions to play the quiz
    # ,will be return jsonify success flag to sucess ,
    # new_question = random questions within the given
    # category not in previous_questions
    def test_quiz_play():
        # define test_quiz_play method
        body = request.get_json()
        # request to get json from frontend and stored in body

        if not ('quiz_category' in body and 'previous_questions' in body):
            # if not found in body will abort error type
            # status code  422 unprocessable
            abort(422)
        previous_questions = body.get('previous_questions')
        # get previous_questions from body store in previous_questions
        quiz_category = body.get('quiz_category')
        # get quiz_category from body store in quiz_category

        try:  # catch error
            category_id = quiz_category['id']
            # to ensure quiz_category['id'] = category_id
            if category_id == 0:  # if category_id is zero empty
                selection = Question.query.filter(
                        # query all questions if not in previous_questions
                        Question.id.notin_((previous_questions))).all()
            else:  # not zero
                selection = Question.query.filter(
                    # query all questions if Question.category == category_id
                    # AND not in previous_questions
                    Question.category == category_id).filter(
                        Question.id.notin_((previous_questions))).all()
            # Resoure =
            # https://stackoverflow.com/questions/26182027/how-to-use-not-in-clause-in-sqlalchemy-orm-query
            new_question = random.choice(selection)
            # function to genarate random question and store in  new_question
            # Resoure = https://pynative.com/python-random-choice/
            avilable_question = len(selection)  # length selection
            if avilable_question > 0:  # if found question
                return jsonify({
                    "success": True,
                    "question": new_question.format()
                })
            else:  # if empty
                return jsonify({
                    "success": True,
                    "question": None
                })
        except Exception:
            # catch error type status code 404 resource not found
            abort(422)

    # Create error handlers for all expected errors
    # Resoure = lesson 3 (Flask Error Handling ) from UDACITY
    @app.errorhandler(404)  # decorator with specify the status code 404
    def resource_not_found(error):  # define method  with parameter  error
        # return jsonify with flag success False,type error,message
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"  # message show in catch error
            }), 404

    @app.errorhandler(422)  # decorator with specify the status code 422
    def unprocessable(error):  # define method  with parameter  error
        # return jsonify with flag success False,type error ,message
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
            }), 422

    @app.errorhandler(400)  # decorator with specify the status code 400
    def bad_request(error):  # define method  with parameter  error
        # return jsonify with flag success False,type error ,message
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
            }), 400

    @app.errorhandler(405)  # decorator with specify the status code 405
    def method_not_allowed(error):  # define method  with parameter  error
        # return jsonify with flag success False,type error ,message
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
            }), 405
    return app
