######################################################################
# Author: Kafui Gle and Jessica Douthit  TODO: Change this to your name
# Username: glek and douthitj   TODO: Change this to your username
#
#  226 Final Project
#
# Purpose: To make a an interactive GUI game
#
#
#######################################################################
# Acknowledgements:
#
# Original code written
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import tkinter as tk
import tkinter.messagebox as mb
import tkinter.simpledialog
import random
import time
import json

class Question:
    """
    Represents a single question in the quiz.

    Attributes:
        text (str): The text of the question.
        answer (str): The correct answer to the question.
        options (list): A list of possible answer options, including the correct one.
    """

    def __init__(self, text, answer, options):
        """
        Initializes a Question object.

        Args:
            text (str): The text of the question.
            answer (str): The correct answer to the question.
            options (list): A list of possible answer options.
        """
        self.text = text
        self.answer = answer
        self.options = options

    def is_correct(self, user_answer):
        """
        Checks if the given answer matches the correct answer.

        Args:
            user_answer (str): The answer provided by the user.

        Returns:
            bool: True if the user's answer is correct, False otherwise.
        """
        return user_answer == self.answer


class Quiz:
    """
    Manages the flow of a trivia quiz.
    """

    def __init__(self, questions):
        """
        Initializes a Quiz object.

        Args:
            questions (list): A list of Question objects.
        """
        self.questions = questions
        self.score = 0
        self.current_question = None
        self.time_remaining = 15  # Seconds per question

        # Load high scores
        self.load_high_scores()

    def load_high_scores(self):
        """Loads high scores from a file (highscores.json)."""
        try:
            with open("highscores.json", "r") as f:
                self.high_scores = json.load(f)
        except FileNotFoundError:
            self.high_scores = []

    def save_high_scores(self):
        """Saves high scores to file (highscores.json)."""
        with open("highscores.json", "w") as f:
            json.dump(self.high_scores, f)

    def get_username(self):
        """Prompts the user for a username."""
        username = tk.simpledialog.askstring("Enter Username", "Please enter your username:")
        return username.strip() or "Anonymous"  # Avoid empty usernames

    def ask_question(self, window):
        """Displays a question, starts the timer, and handles answer submission."""
        if not self.questions:
            self.show_results(window)
            return

        self.current_question = self.questions.pop(0)
        question_label = tk.Label(window, text=self.current_question.text)
        question_label.pack()

        answer_vars = []
        for option in self.current_question.options:
            var = tk.IntVar(value=0)
            answer_vars.append(var)
            radio_button = tk.Radiobutton(window, text=option, variable=var, value=option)
            radio_button.pack()

        def submit_answer():
            selected_answer = None
            for var in answer_vars:
                if var.get() == 1:
                    selected_answer = var.get()
            self.check_answer(selected_answer)

        submit_button = tk.Button(window, text="Submit Answer", command=submit_answer)
        submit_button.pack()

        def start_timer():
            if self.time_remaining > 0:
                timer_label['text'] = f"Time Remaining: {self.time_remaining}"
                self.time_remaining -= 1
                window.after(1000, start_timer)
            else:
                self.check_answer(None)

        timer_label = tk.Label(window)
        timer_label.pack()
        start_timer()

    def check_answer(self, user_answer, window):
        """Check the user's answer."""
        if self.current_question.is_correct(user_answer):
            self.score += 1
        self.ask_question(window)

    def show_results(self, window):
        """Display the quiz results."""
        mb.showinfo("Quiz Finished", f"Your score: {self.score}")
        # Save high score if it's high enough
        if self.score > 0:
            username = self.get_username()
            self.high_scores.append({"username": username, "score": self.score})
            self.save_high_scores()
        window.destroy()


def main():
    # Sample questions
    questions = [
        Question("What is the capital of France?", "Paris", ["Paris", "London", "Berlin", "Madrid"]),
        Question("What is the largest planet in the solar system?", "Jupiter", ["Mercury", "Venus", "Earth", "Jupiter"])
    ]

    # Create the quiz object and start the game
    quiz = Quiz(questions)
    window = tk.Tk()
    quiz.get_username()
    window.title("Tech Trivia Quiz")
    quiz.ask_question(window)
    window.mainloop()


if __name__ == "__main__":
    main()
