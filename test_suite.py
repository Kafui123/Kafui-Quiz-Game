import unittest
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from quiz_data import quiz_data
from m import Quiz
class TestQuizApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def test_display_questions(self):
        app = Quiz(self.root)
        # Ensure the first question is displayed correctly
        self.assertEqual(app.qs_label.cget("text"), quiz_data[0]["question"])

    def test_display_answer_choices(self):
        app = Quiz(self.root)
        # Ensure all answer choices are displayed correctly for the first question
        for i in range(4):
            self.assertEqual(app.choice_btns[i].cget("text"), quiz_data[0]["choices"][i])

    def test_answer_checking_correct(self):
        app = Quiz(self.root)
        # Select the correct answer for the first question
        app.check_answer(quiz_data[0]["choices"].index(quiz_data[0]["answer"]))
        # Ensure score is incremented and "Correct!" feedback is displayed
        self.assertEqual(app.score, 1)
        self.assertEqual(app.feedback_label.cget("text"), "Correct!")

    def test_answer_checking_incorrect(self):
        app = Quiz(self.root)
        # Select an incorrect answer for the first question
        app.check_answer((quiz_data[0]["choices"].index(quiz_data[0]["answer"]) + 1) % 4)
        # Ensure score is not incremented and "Incorrect!" feedback is displayed
        self.assertEqual(app.score, 0)
        self.assertEqual(app.feedback_label.cget("text"), "Incorrect!")

    def test_next_question_navigation(self):
        app = Quiz(self.root)
        # Answer the first question
        app.check_answer(quiz_data[0]["choices"].index(quiz_data[0]["answer"]))
        # Click on the "Next" button
        app.next_question()
        # Ensure the second question is displayed
        self.assertEqual(app.qs_label.cget("text"), quiz_data[1]["question"])

    def test_quiz_completion(self):
        app = Quiz(self.root)
        # Answer all questions
        for question in quiz_data:
            app.check_answer(question["choices"].index(question["answer"]))
            app.next_question()
        # Ensure the completion message is displayed with the final score
        completion_message = "Quiz Completed! Final score: {}/{}".format(app.score, len(quiz_data))
        self.assertTrue(messagebox.showinfo.called)
        self.assertEqual(messagebox.showinfo.call_args[0][1], completion_message)

    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
