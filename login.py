import tkinter as tk
from tkinter import messagebox


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Marching Band Uniform Manager")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Change these to whatever you want
        self.USERNAME = "Jody"
        self.PASSWORD = "PASSWORD"

        self.logged_in = False

        self.build_window()

    def build_window(self):

        title = tk.Label(
            self.root,
            text="Marching Band\nUniform Manager",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        tk.Label(
            self.root,
            text="Username"
        ).pack()

        self.username = tk.Entry(self.root, width=30)
        self.username.pack(pady=5)

        tk.Label(
            self.root,
            text="Password"
        ).pack()

        self.password = tk.Entry(
            self.root,
            show="*",
            width=30
        )
        self.password.pack(pady=5)

        tk.Button(
            self.root,
            text="Login",
            width=20,
            command=self.login
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Exit",
            width=20,
            command=self.root.destroy
        ).pack()

        self.root.bind("<Return>", lambda event: self.login())

    def login(self):

        user = self.username.get().strip()
        pw = self.password.get()

        if user == self.USERNAME and pw == self.PASSWORD:

            self.logged_in = True

            messagebox.showinfo(
                "Success",
                "Login Successful!"
            )

            self.root.destroy()

        else:

            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password."
            )

            self.password.delete(0, tk.END)

    def run(self):

        self.root.mainloop()

        return self.logged_in


# Testing only
if __name__ == "__main__":

    login = LoginWindow()

    if login.run():
        print("Logged In")
    else:
        print("Cancelled")

