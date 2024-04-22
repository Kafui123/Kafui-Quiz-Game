import unittest

from maincode import Question, Quiz


class TestQuiz(unittest.Testcase):
    def setUp(self):
    #This function will set up sample questions for testing
        self.questions = [
            Question("Test Question 1?", "Answer1", ["Answer1","Option 2", "Option 3", "Option 4"]),
        ]

    def test_questions_lading(self):
        # Test if questions are loaded correctly
        quiz = Quiz(self.questions)
        self.assertEqual(len(quiz.questions), 2)

    def test_timer (self):
        # Test answer submission and scoring
        quiz = Quiz(self.questions)


