import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from database import (
    checkout_hat,
    create_database,
    get_hats,
    return_hat,
    search_hats_by_size,
    import_hat_csv,
    export_hat_csv
)


class HatWindow:

    def __init__(self, parent):

        create_database()

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Shako Inventory"
        )

        self.window.geometry(
            "600x600"
        )

        self.build_ui()

        self.load_hats()


    def build_ui(self):

        # -------------------------
        # Title
        # -------------------------

        tk.Label(
            self.window,
            text="Shako Inventory",
            font=("Arial", 20, "bold")
        ).pack(pady=10)


        # -------------------------
        # Table
        # -------------------------

        table_frame = tk.Frame(self.window)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        columns = (
            "ID",
            "Hat Number",
            "Hat Size",
            "Checked Out To"
        )


        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )


        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=120
            )


        self.table.pack(
            fill="both",
            expand=True
        )


        # -------------------------
        # Search
        # -------------------------

        search_frame = tk.Frame(self.window)

        search_frame.pack(pady=5)


        tk.Label(
            search_frame,
            text="Search Hat Size:"
        ).pack(side="left")


        self.search_hat = tk.Entry(
            search_frame,
            width=20
        )

        self.search_hat.pack(
            side="left",
            padx=5
        )


        tk.Button(
            search_frame,
            text="Search",
            command=self.search_hat_inventory
        ).pack(
            side="left"
        )


        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_hats
        ).pack(
            side="left"
        )


        # -------------------------
        # Checkout Name
        # -------------------------

        checkout_frame = tk.Frame(self.window)

        checkout_frame.pack(pady=5)


        tk.Label(
            checkout_frame,
            text="Checked Out To:"
        ).pack(side="left")


        self.person = tk.Entry(
            checkout_frame,
            width=25
        )

        self.person.pack(
            side="left",
            padx=5
        )


        # -------------------------
        # Buttons
        # -------------------------

        button_frame = tk.Frame(self.window)

        button_frame.pack(pady=10)


        tk.Button(
            button_frame,
            text="Import CSV",
            command=self.import_file
        ).grid(
            row=0,
            column=0,
            padx=5
        )


        tk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_file
        ).grid(
            row=0,
            column=1,
            padx=5
        )


        tk.Button(
            button_frame,
            text="Check Out",
            command=self.checkout
        ).grid(
            row=0,
            column=2,
            padx=5
        )


        tk.Button(
            button_frame,
            text="Return",
            command=self.return_selected_hat
        ).grid(
            row=0,
            column=3,
            padx=5
        )


    # -------------------------
    # Load All Hats
    # -------------------------

    def load_hats(self):

        for item in self.table.get_children():

            self.table.delete(item)


        for hat in get_hats():

            self.table.insert(
                "",
                "end",
                values=hat
            )


    # -------------------------
    # Search Hats by Size
    # -------------------------

    def search_hat_inventory(self):

        search = self.search_hat.get().strip()

        for item in self.table.get_children():
            self.table.delete(item)

        if not search:
            self.load_hats()
            return

        hats = search_hats_by_size(search)

        for hat in hats:
            self.table.insert(
                "",
                "end",
                values=hat
            )

    # -------------------------
    # Check Out Hat
    # -------------------------

    def checkout(self):

        selected = self.table.selection()


        if not selected:

            return


        person = self.person.get().strip()


        if not person:

            messagebox.showwarning(
                "Missing Name",
                "Enter the person's name before checking out a hat."
            )

            return


        for item in selected:

            hat_id = self.table.item(
                item,
                "values"
            )[0]


            checkout_hat(
                hat_id,
                person
            )


        self.load_hats()

        self.person.delete(
            0,
            tk.END
        )


    # -------------------------
    # Return Hat
    # -------------------------

    def return_selected_hat(self):

        selected = self.table.selection()


        if not selected:

            return


        for item in selected:

            hat_id = self.table.item(
                item,
                "values"
            )[0]


            return_hat(
                hat_id
            )


        self.load_hats()


    # -------------------------
    # Import CSV
    # -------------------------

    def import_file(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )


        if path:

            import_hat_csv(path)


            messagebox.showinfo(
                "Imported",
                "Hat inventory imported successfully!"
            )


            self.load_hats()


    # -------------------------
    # Export CSV
    # -------------------------

    def export_file(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )


        if path:

            export_hat_csv(path)


            messagebox.showinfo(
                "Exported",
                "Hat inventory exported successfully!"
            )
