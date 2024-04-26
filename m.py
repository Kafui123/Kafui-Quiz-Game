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
from tkinter import messagebox, ttk
from quiz_data import quiz_data
from PIL import Image, ImageTk
from ttkbootstrap import Style

class Quiz:
    """
    Represents a quiz application.

    Attributes:
        root (tk.Tk): The root Tkinter window.
        qs_label (ttk.Label): Label to display the current question.
        choice_btns (list): List of buttons for answer choices.
        feedback_label (ttk.Label): Label to display feedback on answers.
        score (int): The current score of the player.
        score_label (ttk.Label): Label to display the current score.
        next_btn (ttk.Button): Button to move to the next question.
        current_question (int): Index of the current question.
    """
    def __init__(self, root):
        """
        Initializes the QuizApp object.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("600x500")

        # Label to display the current question
        self.qs_label = ttk.Label(
            root,
            anchor="center",
            wraplength=500,
            padding=10
        )
        self.qs_label.pack(pady=10)

        # Load and display image for the first question
        self.image = Image.open("q1.img")  # Replace "q1.jpg" with the actual image path
        self.image = self.image.resize((400, 200))
        self.photo = ImageTk.PhotoImage(self.image)
        self.img_label = tk.Label(root, image=self.photo)
        self.img_label.pack()

        # List of buttons for answer choices
        self.choice_btns = []
        for i in range(4):
            button = ttk.Button(
                root,
                command=lambda i=i: self.check_answer(i)
            )
            button.pack(pady=5)
            self.choice_btns.append(button)

        # Label to display feedback on answers
        self.feedback_label = ttk.Label(
            root,
            anchor="center",
            padding=10
        )
        self.feedback_label.pack(pady=10)

        # Initialize score
        self.score = 0
        # Label to display the current score
        self.score_label = ttk.Label(
            root,
            text="Score: 0/{}".format(len(quiz_data)),
            anchor="center",
            padding=10
        )
        self.score_label.pack(pady=10)

        # Button to move to the next question
        self.next_btn = ttk.Button(
            root,
            text="Next",
            command=self.next_question,
            state="disabled"
        )
        self.next_btn.pack(pady=10)

        # Index of the current question
        self.current_question = 0
        self.show_question()

    def show_question(self):
        """Displays the current question."""
        question = quiz_data[self.current_question]
        self.qs_label.config(text=question["question"])

        choices = question["choices"]
        for i in range(4):
            self.choice_btns[i].config(text=choices[i], state="normal")

        self.feedback_label.config(text="")
        self.next_btn.config(state="disabled")

    def check_answer(self, choice):
        """
        Checks the selected answer and provides feedback.

        Args:
            choice (int): Index of the selected answer choice.
        """
        question = quiz_data[self.current_question]
        selected_choice = self.choice_btns[choice].cget("text")

        if selected_choice == question["answer"]:
            self.score += 1
            self.score_label.config(text="Score: {}/{}".format(self.score, len(quiz_data)))
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text="Incorrect!", foreground="red")

        for button in self.choice_btns:
            button.config(state="disabled")
        self.next_btn.config(state="normal")

    def next_question(self):
        """Moves to the next question."""
        self.current_question += 1

        if self.current_question < len(quiz_data):
            self.show_question()
        else:
            messagebox.showinfo("Quiz Completed",
                                "Quiz Completed! Final score: {}/{}".format(self.score, len(quiz_data)))
            self.root.destroy()


def main():
    """Main function to start the quiz."""
    root = tk.Tk()
    app = Quiz(root)
    root.mainloop()
    style = Style(theme="flatly")

    # Configure the font size for the question and choice buttons
    style.configure("TLabel", font=("Helvetica", 20))
    style.configure("TButton", font=("Helvetica", 16))

if __name__ == "__main__":
    main()
