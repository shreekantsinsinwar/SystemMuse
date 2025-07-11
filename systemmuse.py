import os
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import datetime
import json
import subprocess
import webbrowser

# -------- CONFIGURABLE DATA --------
MOOD_RULES = {
    "code": ["py", "ipynb", "java", "c", "cpp", "js", "ts"],
    "binge": ["mp4", "mkv", "mov", "avi", "mp3"],
    "work": ["xls", "xlsx", "doc", "docx", "ppt", "pptx", "pdf"],
    "web": ["html", "htm", "url"],
    "notes": ["txt", "md", "rtf"],
}

MOOD_MESSAGES = {
    "code": [
        "👨‍💻 Code ninja detected!",
        "🧠 Brainy coder mode: ON",
        "⌨️ Deep Work with your IDE!"
    ],
    "binge": [
        "🎬 Entertainment Overload!",
        "🍿 Netflix and not-so-chill?",
        "🎧 Immersed in audio-visual joy"
    ],
    "work": [
        "📈 Productivity peak hours!",
        "💼 Adulting like a boss",
        "🧾 Meeting docs and deadlines"
    ],
    "web": [
        "🌐 Surfing through the web waves",
        "🕸️ Curious clicker spotted!",
        "🔍 Explorer mode: Active"
    ],
    "notes": [
        "📝 Quiet thinker mode",
        "✍️ Journaling genius",
        "📒 Notes and reflections"
    ],
    "mixed": [
        "🤹 Multitasking marvel!",
        "🔄 Jack of all tabs!",
        "💫 A little bit of everything!"
    ]
}

DATA_FILE = "systemmuse_log.json"

# -------- FUNCTIONALITY --------

def get_yesterday_files_mock():
    # In absence of OS APIs, this uses yesterday’s saved usage
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        all_logs = json.load(f)
    return all_logs.get((datetime.date.today() - datetime.timedelta(days=1)).isoformat(), [])

def determine_mood(files):
    category_count = {k: 0 for k in MOOD_RULES}
    for f in files:
        ext = f.split(".")[-1].lower()
        for cat, exts in MOOD_RULES.items():
            if ext in exts:
                category_count[cat] += 1

    top_cat = max(category_count, key=category_count.get)
    if category_count[top_cat] == 0:
        top_cat = "mixed"
    return random.choice(MOOD_MESSAGES[top_cat])

def open_file(filepath):
    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":
            subprocess.call(["open", filepath])
        else:
            subprocess.call(["xdg-open", filepath])
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file: {e}")

def export_report(mood, files):
    report = f"# SystemMuse Report\n\n**Date:** {datetime.date.today()}\n\n## Mood:\n{mood}\n\n## Files:\n"
    for f in files:
        report += f"- {f}\n"
    save_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md")])
    if save_path:
        with open(save_path, "w") as f:
            f.write(report)
        messagebox.showinfo("Success", "Report exported successfully!")

# -------- GUI --------

class SystemMuseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SystemMuse - Your Usage Moodboard")
        self.root.geometry("600x500")
        self.files = get_yesterday_files_mock()
        self.mood = determine_mood(self.files)

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="🌤️ Your Mood Yesterday:", font=("Helvetica", 14)).pack(pady=10)
        self.mood_label = ttk.Label(self.root, text=self.mood, font=("Helvetica", 12, "italic"), wraplength=500)
        self.mood_label.pack(pady=5)

        ttk.Label(self.root, text="🗂️ Files You Used:", font=("Helvetica", 12, "bold")).pack(pady=10)
        self.file_frame = ttk.Frame(self.root)
        self.file_frame.pack(fill="both", expand=True, padx=20)

        self.file_listbox = tk.Listbox(self.file_frame, selectmode=tk.SINGLE, height=10)
        self.file_listbox.pack(side="left", fill="both", expand=True)
        for f in self.files:
            self.file_listbox.insert(tk.END, f)

        scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(self.root, text="📂 Open Selected", command=self.open_selected).pack(pady=10)
        ttk.Button(self.root, text="📤 Export Mood Report", command=lambda: export_report(self.mood, self.files)).pack(pady=5)

    def open_selected(self):
        selection = self.file_listbox.curselection()
        if selection:
            open_file(self.file_listbox.get(selection[0]))
        else:
            messagebox.showinfo("Select File", "Please select a file to open.")

# -------- MAIN --------

if __name__ == "__main__":
    # For demo: save today’s dummy usage
    today = datetime.date.today().isoformat()
    dummy_files = [
        "/Users/demo/Documents/project.py",
        "/Users/demo/Downloads/movie.mp4",
        "/Users/demo/Documents/report.docx",
        "/Users/demo/Desktop/notes.txt"
    ]
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({today: dummy_files}, f)
    else:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        data[today] = dummy_files
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    root = tk.Tk()
    app = SystemMuseApp(root)
    root.mainloop()

