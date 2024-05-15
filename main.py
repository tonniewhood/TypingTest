
import tkinter as tk

from random import choice


RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


class GUI:

    def __init__(self, root):
        self.root = root
        self.start_button = tk.Button(self.root, text="Start Test", command=self.start_test)
        self.start_button.pack(anchor=tk.CENTER, expand=True)

    def start_test(self):

        self.create_test_widgets()
        with open("story.txt", "r") as file:
            self.texts = file.readlines()
            self.texts = [line for line in self.texts if line != "\n"]

        self.current_text = choice(self.texts)
        self.test_text_entry.insert("1.0", self.current_text)
        self.test_text_entry.config(state=tk.DISABLED)

        self.time = 60
        self.num_words = 0

        self.update_timer()
    
    
    def create_test_widgets(self):

        # Delete the start button
        self.start_button.destroy()

        # Create the test frame
        self.test_frame = tk.Frame(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), bg="red")
        self.test_frame.grid_propagate(False)
        self.test_frame.pack(anchor=tk.CENTER)

        # Create the test text
        self.test_text = tk.Frame(self.test_frame, width=600, height=300, bg="grey")
        self.test_text.grid(row=0, column=1, pady=10)
        self.test_text.pack_propagate(False)
        self.test_text_entry = tk.Text(self.test_text, font=("Arial", 15), wrap=tk.WORD)
        self.test_text_entry.pack()


       # Create the test entry
        self.test_entry_frame = tk.Frame(self.test_frame, width=700, height=450)
        self.test_entry_frame.grid(row=1, column=1, pady=10)
        self.test_entry_frame.pack_propagate(False)
        self.test_entry = tk.Text(self.test_entry_frame, font=("Arial", 15), wrap=tk.WORD)
        self.test_entry.pack()
        self.test_entry.bind("<Key>", self.check_input)


        # Create the test timer
        self.test_timer = tk.Label(self.test_frame, text="Time: 1:00", font=("Helvetica", 30), padx=50)
        self.test_timer.grid(row=0, column=0, pady=10)


    def update_timer(self):
        self.time -= 1

        if self.time == 0:
            self.test_timer.config(text="Time: 0:00")
            self.test_entry.config(state=tk.DISABLED)
            self.display_results()
            return

        minutes = self.time // 60
        seconds = self.time % 60

        if seconds < 10:
            self.test_timer.config(text=f"Time: {minutes}:0{seconds}")
        else:
            self.test_timer.config(text=f"Time: {minutes}:{seconds}")

        self.root.after(1000, self.update_timer)

    def display_results(self):

        # Create the results frame
        self.results = tk.Frame(self.test_frame)
        self.results.grid(row=1, column=0, pady=10)

        # Stick the wpm and the test again buttons in said frame
        self.wpm_label = tk.Label(self.results, text=f"WPM: {self.num_words}", font=("Helvetica", 30))
        self.wpm_label.pack()
        self.test_again_button = tk.Button(self.results, text="Test Again", command=self.test_again)
        self.test_again_button.pack()


    def test_again(self):

        self.test_text_entry.config(state=tk.NORMAL)
        self.test_text_entry.delete("1.0", tk.END)

        self.test_entry.config(state=tk.NORMAL)
        self.test_entry.delete("1.0", tk.END)

        self.results.destroy()
        self.wpm_label.destroy()
        self.test_again_button.destroy()

        self.restart_test()

    def restart_test(self):

        self.current_text = choice(self.texts)
        self.test_text_entry.insert("1.0", self.current_text)
        self.test_text_entry.config(state=tk.DISABLED)

        self.time = 60
        self.num_words = 0

        self.update_timer()


    def check_input(self, event):

        entry = self.test_entry.get("1.0", tk.END)[:-1] + event.char
        words_typed = entry.split()
        words_text = self.current_text.split()

        self.num_words = 0

        for idx in range(len(words_typed)):
            if idx >=len(words_text):
                break

            if words_typed[idx] == words_text[idx]:
                self.num_words += 1


def main():
    root = tk.Tk()
    root.title("Typing Test")
    root.geometry("1000x800")

    gui = GUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()