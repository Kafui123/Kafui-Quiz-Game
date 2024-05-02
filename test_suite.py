import unittest
import tkinter as tk

from tkinter import messagebox
from quiz_data import quiz_data
from m import Quiz
class TestQuizApp(unittest.TestCase):
    """
    Test suite for the Quiz Application
    """

    def setUp(self):
        """
        This function sets up the test environment
        :return:
        """
        self.root = tk.Tk()

    def test_display_questions(self):
        """
        This function tests whether the questions are displayed correctly
        :return:
        """
        app = Quiz(self.root)
        # Ensure the first question is displayed correctly
        self.assertEqual(app.qs_label.cget("text"), quiz_data[0]["question"])

    def test_display_answer_choices(self):
        """
        This function tests whether the answer choices are displayed correctly.
        :return:
        """
        app = Quiz(self.root)
        # Ensure all answer choices are displayed correctly for the first question
        for i in range(4):
            self.assertEqual(app.choice_btns[i].cget("text"), quiz_data[0]["choices"][i])

    def test_answer_checking_correct(self):
        """
        Test checking of correct answers
        :return:
        """

        app = Quiz(self.root)
        # Select the correct answer for the first question
        app.check_answer(quiz_data[0]["choices"].index(quiz_data[0]["answer"]))
        # Ensure score is incremented and "Correct!" feedback is displayed
        self.assertEqual(app.score, 1)
        self.assertEqual(app.feedback_label.cget("text"), "Correct!")

    def test_answer_checking_incorrect(self):
        """
        Test checking for incorrect answers
        :return:
        """
        app = Quiz(self.root)
        # Select an incorrect answer for the first question
        app.check_answer((quiz_data[0]["choices"].index(quiz_data[0]["answer"]) + 1) % 4)
        # Ensure score is not incremented and "Incorrect!" feedback is displayed
        self.assertEqual(app.score, 0)
        self.assertEqual(app.feedback_label.cget("text"), "Incorrect!")

    def test_next_question_navigation(self):
        """
        Test navigation for each question
        :return:
        """
        app = Quiz(self.root)
        # Answer the first question
        app.check_answer(quiz_data[0]["choices"].index(quiz_data[0]["answer"]))
        # Click on the "Next" button
        app.next_question()
        # Ensure the second question is displayed
        self.assertEqual(app.qs_label.cget("text"), quiz_data[1]["question"])

    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
