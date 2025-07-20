Here's a complete GitHub `README.md` file for your **Smart Document Categorizer & Organizer** project:

---

````markdown
📁 Smart Document Categorizer & Organizer

A Python-based desktop application that helps you scan, tag, and organize documents automatically using keyword detection, metadata analysis, and file structure logic. Built using `Tkinter`, this tool is ideal for decluttering your document folders.

---

🚀 Features

- 📄 Supports PDF, DOCX, and TXT files
- 🧠 Automatic Categorization into:
  - `important`
  - `junk`
  - `old`
  - `new`
  - `unused`
  - `current`
- 📂 Organize Files By:
  - Extension (`.pdf`, `.docx`, `.txt`, etc.)
  - Size (small or large files)
  - Last Accessed Date (Less than 10, 20, or more than 20 days)
- 🔑 Keyword-based Categorization
  - Customize important keywords
  - Upload junk keyword list from `.txt` file
- 📆 Date Filtering
  - Scan documents only within a selected range
- 🖥️ Simple GUI Interface
  - Built with Tkinter for easy usability

---

🖼️ GUI Preview

![screenshot](https://drive.google.com/uc?export=view&id=1pkf6zE43rhnhm4VwmzCxnXbJXV59UtIW)

---

📦 Requirements

- Python 3.7+
- Required packages:
  - `PyPDF2`
  - `python-docx`
  - `tkinter` (comes with standard Python)
  
To install dependencies:
```bash
pip install PyPDF2 python-docx
````

---

## 🛠️ How to Use

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/document-categorizer.git
   cd document-categorizer
   ```

2. Run the script:

   ```bash
   python categorizer.py
   ```

3. From the GUI:

   * Select a folder containing documents
   * Choose date range and keywords
   * Load junk keyword file (optional)
   * Click "Start Scanning"
   * Review results and organize files by Extension, Size, or Date

---

## 📊 Accuracy Measurement (Optional for Advanced Users)

To measure model accuracy:

1. Manually label \~100 test files.
2. Compare predicted vs expected tags.
3. Use these metrics:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1 Score  = 2 * (Precision * Recall) / (Precision + Recall)
```

---

## 🧠 How Categorization Works

* **Important**:

  * Detected based on keywords or sensitive data (Aadhaar, PAN, Email, etc.)
* **Junk**:

  * Short documents, lorem ipsum, specific keywords, small size, or out-of-range dates
* **Old**:

  * Created more than 3 years ago
* **New**:

  * Modified recently (within the past year)
* **Unused**:

  * Not accessed in over 1 year
* **Current**:

  * Everything else

---

## 📁 Folder Structure

```plaintext
documents/
├── marksheet.pdf
├── bank_statement.docx
├── ...
```

After scanning and organizing, files may be moved into subfolders like:

```plaintext
documents/
├── .pdf/
├── moreThan100KB/
├── Less than 10 Days/
```

---

## 📌 To-Do / Enhancements

* [ ] Add support for cloud storage (AWS S3, GDrive)
* [ ] Add export report (.csv or .json)
* [ ] Add auto-tag suggestions using ML
* [ ] Dark mode UI
