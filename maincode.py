######################################################################
# Author: Kafui Gle and Jessica Douthit
# Username: glek and douthitj
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
    Represents  the questions in the quiz.

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
        self.score_label = None  # This initializes the score variable
        self.questions = questions
        self.score = 0
        self.current_question = None
        self.time_remaining = 15  # Seconds per question
        self.timer_id = None  # To store the ID of the timer

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


        # Remove previous question and answer widgets
        for widget in window.winfo_children():
            widget.destroy()

        self.current_question = self.questions.pop(0)
        question_label = tk.Label(window, text=self.current_question.text)
        question_label.pack()

        answer_vars = []
        for option in self.current_question.options:
            var = tk.StringVar()
            answer_vars.append(var)
            radio_button = tk.Radiobutton(window, text=option, value=option)
            radio_button.pack()

        print(self.score_label)
        # Creation of the score label
        if self.score_label is None:
            self.score_label = tk.Label(window, text="Score: 0")
            self.score_label.pack()



        def submit_answer():
            selected_answer = None
            for var in answer_vars:
                if var.get():
                    selected_answer = var.get()
            self.check_answer(selected_answer, window)

        submit_button = tk.Button(window, text="Submit Answer", command=submit_answer)
        submit_button.pack()

        # Start the timer for the current question
        self.time_remaining = 15
        self.start_timer(window)

    def start_timer(self, window):
        """Starts the timer for the current question."""
        if self.timer_id:
            window.after_cancel(self.timer_id)
        if self.time_remaining > 0:
            timer_label = tk.Label(window)
            timer_label.pack()
            timer_label['text'] = f"Time Remaining: {self.time_remaining}"
            self.time_remaining -= 1
            self.timer_id = window.after(1000, self.start_timer, window)

        else:
            self.check_answer(None, window)

    def check_answer(self, user_answer, window):
        """Check the user's answer."""
        if self.current_question.is_correct(user_answer):
            self.score += 1
            self.score_label['text'] = f"Score: {self.score}"
        self.ask_question(window)  # Move to the next question

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
        Question("What is the largest planet in the solar system?", "Jupiter", ["Mercury", "Venus", "Earth", "Jupiter"]),
        Question("What is the capital of Australia?", "Canberra", ["Canberra", "Sydney", "Melbourne", "Darwin"]),
        Question("What is the coldest season?", "Winter", ["Summer", "Fall", "Winter", "Spring"]),
        Question("What is the warmest season?", "Summer", ["Summer", "Fall", "Winter", "Spring"]),
        Question("What is the largest continent?", "Asia", ["Europe", "Asia", "Africa", "North America"]),
        Question("Which of the following is a primary color?", "Red", ["Red", "Cyan", "Magenta", "Black"]),
        Question("Which college do the creators of this quiz attend?", "Berea College", ["Vanderbilt", "College of the Ozarks", "Berea College", "University of Kentucky"]),
        Question("What is the to layer of the earth?", "Crust", ["Mantle", "Outer Core", "Inner Core", "Crust"]),
        Question("Which of the following borders Russia?", "Winter", ["Canada", "Ukraine", "Mexico", "Thailand"]),
    ]

    # Create the quiz object and start the game
    quiz = Quiz(questions)
    window = tk.Tk()
    quiz.get_username()
    window.title("Tech Trivia Quiz")
    quiz.ask_question(window)

    # Add score display label
    score_display_label = tk.Label(window, text="Score: 0")
    score_display_label.place(x=300, y=20)  # Place the label at the top-right corner
    quiz.score_label = score_display_label

    window.mainloop()


if __name__ == "__main__":
    main()



