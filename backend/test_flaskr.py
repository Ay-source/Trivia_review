import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        #Get environment variables
        load_dotenv()
        self.host = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'postgres')
        self.database_name = os.getenv('DB_TEST_NAME', 'trivia_test')
        self.database_path = "postgresql://{}:{}@{}/{}".\
        format(self.user, self.password,self.host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])

    def test_405_get_categories(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method not Allowed")

    def test_get_questions(self):
        res = self.client().get("/questions", json={"page":1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"], None)

    def test_404_get_questions(self):
        res = self.client().get("/questions?page=20")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource not Found")
    
    def test_delete_delete_questions(self):
        res = self.client().delete("/questions/5")
        data= json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_422_delete_delete_questions(self):
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_post_post_question(self):
        res = self.client().post("/questions", 
        json={
            "question": "What is my name?", 
            "answer": "Ayomide", 
            "difficulty": 2, 
            "category": "1"
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        
    def test_422_post_post_question(self):
        res = self.client().post("/questions", 
        json={
            "question": "What is my name?", 
            "answer": "Ayomide", 
            "difficulty": 2, 
            "category": "Arts"
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_400_post_post_question(self):
        res = self.client().post("/questions", 
        json={
            "question": "What is my name?", 
            "answer": "Ayomide", 
            "difficulty": 2, 
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "Bad Request")

    def test_post_search_questions(self):
        res = self.client().post("/questions", json={"searchTerm":"how"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])

    def test_400_post_search_questions(self):
        res = self.client().post("/questions", 
        json={
            "searchTerm":"",
            "question": "What is my name?", 
            "answer": "Ayomide", 
            "difficulty": 2, 
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "Bad Request")

    def test_get_categorized_questions(self):
        res = self.client().get("/categories/1/questions")

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])

    def test_405_get_categorized_questions(self):
        res = self.client().post("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method not Allowed")

    def test_post_quizzes(self):
        res = self.client().post("/quizzes", 
        json={
            "previous_questions":[21,17], 
            "quiz_category":{
                "id":0, 
                "type":"click"
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])

    def test_405_post_quizzes(self):
        res = self.client().get("/quizzes")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method not Allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()