import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

from myfunc import split_block, parse_block, saveexcel

class ERAN(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ERAN - KGET Processor")
        self.geometry("500x200")
        self.icon = tk.PhotoImage(file="images\\eran-icon32.png")# Load PNG
        self.iconphoto(False, self.icon)

        # Set window background color
        self.configure(bg="#2a2c3b")

        # Create frames with window background color
        top_frame = tk.Frame(self, bg="#2a2c3b")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        bottom_frame = tk.Frame(self, bg="#2a2c3b")
        bottom_frame.pack(side="top", fill="x", padx=10, pady=10)

        button_frame = tk.Frame(self, bg="#2a2c3b")
        button_frame.pack(side="top", fill="x", padx=10, pady=10)

        status_frame = tk.Frame(self, relief="sunken", bd=1, bg="#313445")
        status_frame.pack(side="bottom", fill="x", padx=10, pady=5)


        # Load PNG icon for the button
        self.select_icon = tk.PhotoImage(file="images\\select_icon.png") #ImageTk.PhotoImage(Image.open("select_icon.png").resize((24, 24)))  # Load PNG
        self.folder_icon = tk.PhotoImage(file="images\\save_icon.png") #ImageTk.PhotoImage(Image.open("save_icon.png").resize((24, 24)))  # Load PNG


        # Status label on the left and Select button with icon on the right
        self.file_var = tk.StringVar()
        self.file_var.set(" Select ENM Kget log(s) to start")

        log_file_button = tk.Button(top_frame, image=self.select_icon, textvariable=self.file_var, compound="left", anchor="w", command=self.select_log_files, relief="flat", bg="#313445", fg="#c2caeb")
        log_file_button.pack(fill="x")

        # Export label and Export button on the same row
        self.folder_var = tk.StringVar()
        self.folder_var.set(" Save exported MO to")

        folder_button = tk.Button(bottom_frame, image=self.folder_icon, textvariable=self.folder_var, compound="left", anchor = "w", command=self.save_export_file, relief="flat", bg="#313445", fg="#c2caeb")
        folder_button.pack(fill="x")

        # Start button
        export_button = tk.Button(button_frame, text="Export", anchor="center", command=self.export, bg="#313445", fg="#c2caeb", width=10)
        export_button.pack(padx=10, anchor="e")

        # Status bar for dynamic updates
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(status_frame, textvariable=self.status_var, anchor="w",
                                bg="#313445", fg="#c2caeb")
        status_label.pack(side="left", fill="x")

        # Store selected log files
        self.selected_files = []
        self.outfile = ""

    def select_log_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Log Files",
            filetypes=[("Log Files", "*.log")],
        )

        if file_paths:
            self.selected_files = list(file_paths)
            file_names = ', '.join([file.split('/')[-1] for file in file_paths])
            self.status_var.set(f"Selected files: {file_names}")
            self.file_var.set(f" Selected files: {file_names}")
        else:
            self.status_var.set("No files selected")


    def save_export_file(self):
        if not self.selected_files:
            messagebox.showwarning("No log selected", "Please select log file(s) to start.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Export File",
            defaultextension=".xlsx",
            filetypes=[("Microsoft Excel", "*.xlsx")],
        )
        if file_path:
            self.outfile = file_path
            self.status_var.set(f"Export as {file_path}")
            self.folder_var.set(f" Export as {file_path}")
        else:
            self.status_var.set("Save operation cancelled")


    def export (self):
        if not self.selected_files:
            messagebox.showwarning("No log selected", "Please select log file(s) to start.")
            return

        if not self.outfile:
            messagebox.showwarning("No export file selected", "Please select location to save file as")

        # # print ("Spliting blocks...")
        self.status_var.set("Spliting MO blocks...")
        blocks = [split_block(file) for file in self.selected_files]

        # #array of all MO block (id, MO, block data)
        self.status_var.set("Concating MO blocks from multiple logs...")
        BLOCKS = np.concatenate(blocks)

        # #parse block into dict of param: value, with MOCLass as first array column
        self.status_var.set("Parsing MO blocks into row data...")
        BLOCKS = np.array([parse_block(block) for block in BLOCKS])

        # print (f"Saving excel data to {filepath}...")
        self.status_var.set("Saving parsed MO data to excel file.")
        saveexcel(self.outfile, BLOCKS)

        self.status_var.set(f"Complete! Export MO is saved to {self.outfile}")

if __name__ == "__main__":
    app = ERAN()
    app.mainloop()
