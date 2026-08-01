"""
main.py
Marching Band Uniform Manager
"""

import tkinter as tk
from hat_inventory import HatWindow
from login import LoginWindow
from inventory import InventoryWindow
from database import create_database


class UniformManagerApp:

    def __init__(self):

        # Make sure database exists
        create_database()

        self.root = tk.Tk()

        self.root.title(
            "Marching Band Uniform Manager"
        )

        self.root.geometry(
            "600x600"
        )

        self.root.resizable(
            True,
            True
        )


        self.build_ui()


    def build_ui(self):

        # -------------------------
        # Title
        # -------------------------

        title = tk.Label(
            self.root,
            text="🎺 Marching Band Uniform Manager",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=30
        )


        # -------------------------
        # Buttons
        # -------------------------

        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=20
        )


        tk.Button(
            button_frame,
            text="Open Inventory",
            width=50,
            height=4,
            command=self.open_inventory
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )


        tk.Button(
            button_frame,
            text="Exit",
            width=50,
            height=4,
            command=self.root.destroy
        ).grid(
            row=2,
            column=0,
            padx=20,
            pady=20
        )

        tk.Button(
            button_frame,
            text="Hat Inventory",
            width=50,
            height=4,
            command=lambda: HatWindow(self.root)
        ).grid(
            row=3,
            column=0,
            padx=20,
            pady=20
)
        # -------------------------
        # Status
        # -------------------------

        self.status = tk.Label(
            self.root,
            text="Ready",
            relief="sunken",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            side="bottom"
        )


    def open_inventory(self):

        InventoryWindow(
            self.root
        )


    def run(self):

        self.root.mainloop()



# ===================================
# Program Start
# ===================================

def main():

    login = LoginWindow()


    if login.run():

        app = UniformManagerApp()

        app.run()


    else:

        print(
            "Login cancelled."
        )



if __name__ == "__main__":

    main()

