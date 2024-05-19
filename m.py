######################################################################
# Author: Kafui Gle
#
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
        # This code converts the resized image stored into a suitable format because tkinter does not support
        # Pil images
        self.photo = ImageTk.PhotoImage(self.image)
        self.img_label = tk.Label(root, image=self.photo)
        self.img_label.pack()

        # List of buttons for answer choices
        self.choice_btns = []
        for i in range(4):
            button = ttk.Button(
                root,
                command=lambda i=i: self.check_answer(i)  # The command parameter specifies the function to be called
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
        """Displays the current question and sets up the answer choices for them respectively """
        question = quiz_data[self.current_question]
        self.qs_label.config(text=question["question"])

        choices = question["choices"]   # This gets the choice values from the quiz_data.py file
        for i in range(4):
            self.choice_btns[i].config(text=choices[i], state="normal")

        self.feedback_label.config(text="")  # This code ensures that the text displayed inside the
        #  feedback label is cleared after the user clicks on the next button

        self.next_btn.config(state="disabled")   # When it moves to the next question it disables the next button
        # so it forces the user to click an option

        try:
            image_path = f"q{self.current_question + 1}.img"  # This code changes the image with each new question
            self.image = Image.open(image_path)  # This code opens the image using the Image.open function from the PIL
            self.image = self.image.resize((400, 200))
            self.photo = ImageTk.PhotoImage(self.image)
            self.img_label.config(image=self.photo)
        except FileNotFoundError:
            print()

    def check_answer(self, choice):
        """
        Checks the selected answer and provides feedback.

        Args:
            choice (int): Index of the selected answer choice.
        """
        question = quiz_data[self.current_question]
        selected_choice = self.choice_btns[choice].cget("text")  # We used .cget() here so that we could obtain the text
        # from the configured value

        if selected_choice == question["answer"]:
            self.score += 1
            self.score_label.config(text="Score: {}/{}".format(self.score, len(quiz_data)))  # The .format is used
            # here to directly insert values into strings in python
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text="Incorrect!", foreground="red")
        # After the feedback displays whether it is correct or not, the buttons of the option choices
        # then become disabled.
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
    style = Style(theme="flatly")

    # Configure the font size for the question and choice buttons
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 10))
    root.mainloop()



if __name__ == "__main__":
    main()
