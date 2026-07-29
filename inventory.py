"""
inventory.py
Marching Band Uniform Manager
Part 1 - Inventory Window Layout
"""


import tkinter as tk
import csv
from tkinter import ttk, filedialog, messagebox
from database import import_csv
from database import delete_uniform

from database import (
    get_uniforms,
    get_statistics,
    create_database,
    checkout_uniform,
    return_uniform

)


class InventoryWindow:

    def __init__(self, parent):

        create_database()

        self.window = tk.Toplevel(parent)

        self.window.title("Uniform Inventory")
        self.window.geometry("1100x650")
        self.window.minsize(900, 500)

        self.build_ui()

        print("Table created:", hasattr(self, "table"))

        self.load_inventory()

    # ==========================
    # Update Statistics
    # ==========================



    def build_ui(self):

        # Title
        tk.Label(
            self.window,
            text="Uniform Inventory",
            font=("Arial", 20, "bold")
        ).pack(pady=10)


        # Table
        table_frame = tk.Frame(self.window)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        columns = (
            "ID",
            "Number",
            "Height",
            "Waist",
            "Seat",
            "Neck",
            "Neck To Seat",
            "Sleeve",
            "Inseam",
            "Outseam",
            "Gender",
            "Hat",
            "Checked Out To"
        )


        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        self.table.column(
            "ID",
            width=0,
            stretch=False
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            if column != "ID":
                self.table.column(
                    column,
                    width=90
                )

        self.table.pack(
            fill="both",
            expand=True
        )


        # Buttons
        checkout_frame = tk.Frame(self.window)
        checkout_frame.pack(pady=5)


        tk.Label(
            checkout_frame,
            text="Checked Out To:"
        ).pack(side="left")


        self.checkout_name = tk.Entry(
            checkout_frame,
            width=25
        )

        self.checkout_name.pack(
            side="left",
            padx=5
        )

 

        # ==========================
        # Search Area
        # ==========================

        search_frame = tk.LabelFrame(
        self.window,
        text="Search Measurements"
        )

        search_frame.pack(
        fill="x",
        padx=10,
        pady=5
        )


        tk.Label(search_frame, text="Height").grid(row=0,column=0)
        self.search_height = tk.Entry(search_frame,width=8)
        self.search_height.grid(row=0,column=1)


        tk.Label(search_frame, text="Waist").grid(row=0,column=2)
        self.search_waist = tk.Entry(search_frame,width=8)
        self.search_waist.grid(row=0,column=3)


        tk.Label(search_frame, text="Seat").grid(row=0,column=4)
        self.search_seat = tk.Entry(search_frame,width=8)
        self.search_seat.grid(row=0,column=5)


        tk.Label(search_frame,text="Gender").grid(row=0,column=6)

        self.search_gender = ttk.Combobox(
        search_frame,
        values=["","M","F"],
        width=5
        )

        self.search_gender.grid(row=0,column=7)


        self.available_only = tk.BooleanVar()

        tk.Checkbutton(
        search_frame,
        text="Available Only",
        variable=self.available_only
        ).grid(row=0,column=8)


        tk.Button(
        search_frame,
        text="Search",
        command=self.search_uniforms
        ).grid(row=0,column=9,padx=5)


        tk.Button(
        search_frame,
        text="Show All",
        command=self.load_inventory
        ).grid(row=0,column=10)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)


        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_inventory
        ).grid(row=0, column=0, padx=5)


        tk.Button(
            button_frame,
            text="Import CSV",
            command=self.import_file
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_file
        ).grid(row=0, column=2, padx=5)
        

        tk.Button(
            button_frame,
            text="Check Out",
            command=self.checkout_selected
        ).grid(row=0, column=3, padx=5)


        tk.Button(
            button_frame,
            text="Return",
            command=self.return_selected
        ).grid(row=0, column=4, padx=5)

        # Status
        self.status = tk.Label(
            self.window,
            text="Total Uniforms: 0",
            relief="sunken",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            side="bottom"
        )
    def load_inventory(self):

        # Clear current table
        for item in self.table.get_children():
            self.table.delete(item)


        uniforms = get_uniforms()

        print("Loaded uniforms:", len(uniforms))


        for uniform in uniforms:

            (
                db_id,
                number,
                height,
                waist,
                seat,
                neck,
                neck_to_seat,
                sleeve,
                inseam,
                outseam,
                gender,
                hat_number,
                checked_out_to
            ) = uniform


            self.table.insert(
                "",
                "end",
                values=(
                    db_id,
                    number,
                    height,
                    waist,
                    seat,
                    neck,
                    neck_to_seat,
                    sleeve,
                    inseam,
                    outseam,
                    gender,
                    hat_number,
                    checked_out_to
                )
            )
            self.update_status()
       

    def update_status(self):

        total, available, checked = get_statistics()


        self.status.config(
            text=
            f"Total Uniforms: {total} | "
            f"Available: {available} | "
            f"Checked Out: {checked}"
        )


    def import_file(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )


        if path:

            import_csv(path)

            messagebox.showinfo(
                "Imported",
                "Uniforms imported successfully!"
            )

            self.load_inventory()


    def export_file(self):

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if save_path:

            uniforms = get_uniforms()

            with open(
                save_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "ID",
                    "Number",
                    "Height",
                    "Waist",
                    "Seat",
                    "Neck",
                    "Neck To Seat",
                    "Sleeve",
                    "Inseam",
                    "Outseam",
                    "Gender",
                    "Hat Number",
                    "Checked Out To"
                ])

                for uniform in uniforms:
                    writer.writerow(uniform)


            messagebox.showinfo(
                "Export Complete",
                "Inventory exported successfully!"
            )

    def checkout_selected(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a uniform to checkout.")
            return

        person = self.checkout_name.get()

        if not person:
            messagebox.showwarning("Warning", "Please enter a name for the person checking out the uniform.")
            return

        for item in selected:
            values = self.table.item(item, "values")
            uniform_id = values[0]

            checkout_uniform(uniform_id, person)

        self.load_inventory()
        self.checkout_name.delete(0, tk.END)


    def return_selected(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a uniform to return.")
            return

        for item in selected:
            values = self.table.item(item, "values")
            uniform_id = values[0]

            return_uniform(uniform_id)

        self.load_inventory()
        

    # ==========================
    # SEARCH FUNCTION
    # ==========================

        # ==========================
    # SEARCH FUNCTION
    # ==========================

    def search_uniforms(self):

        # Clear table
        for item in self.table.get_children():
            self.table.delete(item)


        uniforms = get_uniforms()


        # Get target measurements
        try:
            target_height = float(self.search_height.get())
            target_waist = float(self.search_waist.get())
            target_seat = float(self.search_seat.get())

        except ValueError:
            messagebox.showwarning(
                "Missing Measurements",
                "Enter height, waist, and seat measurements."
            )
            return


        gender = self.search_gender.get()


        matches = []


        # Compare uniforms
        for uniform in uniforms:

            (
                db_id,
                number,
                height,
                waist,
                seat,
                neck,
                neck_to_seat,
                sleeve,
                inseam,
                outseam,
                u_gender,
                hat,
                checked_out
            ) = uniform


            # Available filter
            if self.available_only.get() and checked_out != "":
                continue


            # Gender filter
            if gender and gender != u_gender:
                continue


            # Calculate fit score
            score = (
                abs(height - target_height)
                +
                abs(waist - target_waist)
                +
                abs(seat - target_seat)
            )


            matches.append(
                (score, uniform)
            )


        # Closest first
        matches.sort(
            key=lambda x: x[0]
        )


        # Only show top 10
        matches = matches[:10]


        # Create colors
        self.table.tag_configure(
            "good",
            background="lightgreen"
        )

        self.table.tag_configure(
            "okay",
            background="khaki"
        )

        self.table.tag_configure(
            "bad",
            background="salmon"
        )


        # Display results
        for score, uniform in matches:

            (
                db_id,
                number,
                height,
                waist,
                seat,
                neck,
                neck_to_seat,
                sleeve,
                inseam,
                outseam,
                gender,
                hat,
                checked_out
            ) = uniform


            row = self.table.insert(
                "",
                "end",
                values=(
                    db_id,
                    number,
                    height,
                    waist,
                    seat,
                    neck,
                    neck_to_seat,
                    sleeve,
                    inseam,
                    outseam,
                    gender,
                    hat,
                    checked_out
                )
            )


            # Color match quality
            if score <= 3:
                self.table.item(
                    row,
                    tags=("good",)
                )

            elif score <= 8:
                self.table.item(
                    row,
                    tags=("okay",)
                )

            else:
                self.table.item(
                    row,
                    tags=("bad",)
                )
# Testing window only
if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    InventoryWindow(root)

    root.mainloop()