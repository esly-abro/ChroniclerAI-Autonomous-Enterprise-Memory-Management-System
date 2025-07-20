import os
import shutil
import math
import datetime
import re
import string
import time
from tkinter import Tk, Label, Entry, Button, filedialog, Text, END
from tkinter import messagebox
from PyPDF2 import PdfReader
from docx import Document

# ---------- Global Constants ----------
DOCUMENTS_FOLDER = "./documents"
IMPORTANT_KEYWORDS = set()
IMPORTANT_PHRASES = ["confidential report", "bank statement", "marksheet", "payment receipt"]
JUNK_KEYWORDS = set()
FROM_DATE = datetime.datetime.min
TO_DATE = datetime.datetime.max
FOLDER_PATH = DOCUMENTS_FOLDER  # Default folder


# ---------- File Text Extraction ----------
def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            return " ".join(page.extract_text() or "" for page in reader.pages)
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            return " ".join(para.text for para in doc.paragraphs)
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception:
        return ""
    return ""

# ---------- Categorization Logic ----------
def contains_sensitive_patterns(text):
    patterns = [
        r"\b\d{4} \d{4} \d{4}\b",  # Aadhaar
        r"\b[A-Z]{5}\d{4}[A-Z]\b",  # PAN
        r"\b\d{10}\b",  # Phone
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"  # Email
    ]
    return any(re.search(p, text) for p in patterns)

def get_file_metadata(file_path):
    stat = os.stat(file_path)
    return (
        datetime.datetime.fromtimestamp(stat.st_ctime),
        datetime.datetime.fromtimestamp(stat.st_mtime),
        datetime.datetime.fromtimestamp(stat.st_atime)
    )

def categorize(file_path, text, created, modified, accessed):
    tokens = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    tokens = [t for t in tokens if t.isalnum()]
    word_set = set(tokens)
    current_year = datetime.datetime.now().year

    if IMPORTANT_KEYWORDS & word_set or contains_sensitive_patterns(text):
        return ["important"]
    for phrase in IMPORTANT_PHRASES:
        if phrase in text.lower():
            return ["important"]
    if len(tokens) < 30 or "lorem ipsum" in text.lower():
        return ["junk"]
    if os.path.getsize(file_path) < 5000:
        return ["junk"]
    if JUNK_KEYWORDS & word_set:
        return ["junk"]
    if FROM_DATE <= created <= TO_DATE:
        return ["junk"]
    if created.year < current_year - 3:
        return ["old"]
    if modified.year >= current_year - 1:
        return ["new"]
    if (datetime.datetime.now() - accessed).days > 365:
        return ["unused"]
    return ["current"]

# ---------- GUI Actions ----------
def browse_folder():
    global FOLDER_PATH
    FOLDER_PATH = filedialog.askdirectory()
    folder_label.config(text=FOLDER_PATH)

def load_junk_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as jf:
            for line in jf:
                word = line.strip().lower()
                if word:
                    JUNK_KEYWORDS.add(word)
        junk_label.config(text="Junk file loaded ✅")

def start_scan():
    global FROM_DATE, TO_DATE, IMPORTANT_KEYWORDS
    try:
        FROM_DATE = datetime.datetime.strptime(from_date_entry.get(), "%Y-%m-%d")
        TO_DATE = datetime.datetime.strptime(to_date_entry.get(), "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter valid dates in YYYY-MM-DD format.")
        return

    important_input = important_entry.get()
    if important_input:
        IMPORTANT_KEYWORDS = {word.strip().lower() for word in important_input.split(",")}

    if not FOLDER_PATH or not os.path.exists(FOLDER_PATH):
        messagebox.showerror("Folder Missing", "Please choose a valid folder to scan.")
        return

    output_box.delete(1.0, END)
    scanning_label.config(text="⏳ Scanning files, please wait...")
    root.update()

    file_count = 0
    for file_name in os.listdir(FOLDER_PATH):
        if file_name.lower().endswith((".pdf", ".docx", ".txt")):
            full_path = os.path.join(FOLDER_PATH, file_name)
            text = extract_text(full_path)
            created, modified, accessed = get_file_metadata(full_path)
            tags = categorize(full_path, text, created, modified, accessed)

            output_box.insert(END, f"{file_name} --> Tag: {tags[0]} | Created: {created.date()} | Modified: {modified.date()}\n")
            root.update()
            time.sleep(0.2)
            file_count += 1

    if file_count == 0:
        output_box.insert(END, "No valid files (.pdf, .docx, .txt) found in the folder.\n")

    scanning_label.config(text="✅ Scan complete!")

# ---------- File Organizers ----------
def checkFile(filename):
    return filename == os.path.basename(__file__)

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s_%s" % (round(s), size_name[i])

def organize_by_extension():
    try:
        all_files = os.listdir(FOLDER_PATH)
        exts = set(os.path.splitext(f)[1] for f in all_files if '.' in f)
        for ext in exts:
            if ext:
                os.makedirs(os.path.join(FOLDER_PATH, ext), exist_ok=True)
        for f in all_files:
            ext = os.path.splitext(f)[1]
            src = os.path.join(FOLDER_PATH, f)
            dst = os.path.join(FOLDER_PATH, ext, f)
            if os.path.isfile(src):
                shutil.move(src, dst)
        messagebox.showinfo("Done", "Files organized by extension.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def organize_by_size():
    try:
        files = [f for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f)) and not checkFile(f)]
        for f in files:
            size = convert_size(os.stat(os.path.join(FOLDER_PATH, f)).st_size)
            size_val, unit = size.split("_")
            size_folder = "lessThan50" + unit if int(size_val) < 50 else "moreThan100" + unit
            os.makedirs(os.path.join(FOLDER_PATH, size_folder), exist_ok=True)
            shutil.move(os.path.join(FOLDER_PATH, f), os.path.join(FOLDER_PATH, size_folder, f))
        messagebox.showinfo("Done", "Files organized by size.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def organize_by_date():
    try:
        for f in os.listdir(FOLDER_PATH):
            full_path = os.path.join(FOLDER_PATH, f)
            if os.path.isfile(full_path) and not checkFile(f):
                access_time = os.stat(full_path).st_atime
                days_diff = (datetime.datetime.now() - datetime.datetime.fromtimestamp(access_time)).days
                if days_diff < 10:
                    folder = "Less than 10 Days"
                elif days_diff < 20:
                    folder = "Less than 20 Days"
                else:
                    folder = "More than 20 Days"
                os.makedirs(os.path.join(FOLDER_PATH, folder), exist_ok=True)
                shutil.move(full_path, os.path.join(FOLDER_PATH, folder, f))
        messagebox.showinfo("Done", "Files organized by date accessed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------- GUI Layout ----------
root = Tk()
root.title("📁 Smart Document Categorizer & Organizer")
root.geometry("850x650")

Label(root, text="Folder:").pack()
folder_label = Label(root, text=FOLDER_PATH, fg="blue")
folder_label.pack()

Button(root, text="Browse Folder", command=browse_folder).pack()

Label(root, text="From Date (YYYY-MM-DD):").pack()
from_date_entry = Entry(root)
from_date_entry.insert(0, "2010-01-01")
from_date_entry.pack()

Label(root, text="To Date (YYYY-MM-DD):").pack()
to_date_entry = Entry(root)
to_date_entry.insert(0, "2030-12-31")
to_date_entry.pack()

Label(root, text="Important Keywords (comma-separated):").pack()
important_entry = Entry(root, width=60)
important_entry.insert(0, "confidential, bank, marksheet, username, password")
important_entry.pack(pady=5)

Label(root, text="Upload Junk Keywords File (.txt):").pack()
Button(root, text="Load Junk File", command=load_junk_file).pack()
junk_label = Label(root, text="No file loaded", fg="green")
junk_label.pack(pady=5)

scanning_label = Label(root, text="", fg="orange")
scanning_label.pack()

Button(root, text="🔍 Start Scanning", command=start_scan, bg="lightgreen").pack(pady=10)

output_box = Text(root, height=15, width=100)
output_box.pack()

# New Buttons for Organizing
Button(root, text="📂 Organize by Extension", command=organize_by_extension).pack(pady=2)
Button(root, text="📏 Organize by Size", command=organize_by_size).pack(pady=2)
Button(root, text="🕒 Organize by Date Accessed", command=organize_by_date).pack(pady=2)

root.mainloop()
