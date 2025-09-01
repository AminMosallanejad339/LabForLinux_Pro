# 🧠 Linux Practice Lab

An interactive **Linux practice environment** built with [Streamlit](https://streamlit.io/).  
This app loads CSV question sets, displays one question at a time, and lets you type and submit Linux queries to check against the correct answer.

---

## ✨ Features
- 📂 **CSV-based question sets** – easy to add or edit.
- 🌓 **Dark/Light mode toggle**.
- 📊 **Progress tracking** for the current file.
- ⏩ **Navigation**: Next/Previous buttons and jump to any question.
- ✅ **Answer checking** – instant feedback.
- ⌨️ **Keyboard shortcuts** for faster practice.

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/AminMosallanejad339/linux-lab-.git
cd linux-lab-
```

### 2️⃣ Install dependencies
Make sure you have **Python 3.8+** installed.

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
streamlit
pandas
```

---

## 📂 Prepare Your Questions
1. Create a folder named **`directfolder`** in the project root.
2. Inside it, place your CSV files containing the questions.



## 📄 Sample CSV (save as `directfolder/sample.csv`)
```csv
question,answer,explanation
"How to display CPU and memory usage per process?","top or ps aux","Shows resource usage by each process."
"How to see process environment variables?","cat /proc/PID/environ","Displays environment variables for the process."
"How to get process tree including children?","pstree -p PID","Shows process tree starting at given PID."
```

---

## ▶️ Run the App
From the project root folder, run:
```bash
streamlit run app.py
```
*(Replace `app.py` with your actual filename if different)*

---

## 🎮 Usage
1. Select a question set from the **left sidebar**.
2. Read the question and type your Linux in the answer box.
3. **Submit**:
   - Press `Ctrl+Enter`  
   - or click the **✅ Submit** button
4. Navigation shortcuts:
   - `Alt+a` → Show Answer  
   - `Alt+n` → Next Question  
   - `Alt+p` → Previous Question  

---

## 🖤 Dark Mode
Toggle dark mode using the switch in the main app.

---

## 📁 Project Structure
```
linux-Linux-lab/
│
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── directfolder/          # CSV question sets
│   ├── sample.csv
│   ├── set1.csv
│   └── ...
```

---

## 📜 License
MIT License – free to use, modify, and share.

---

## 🙌 Credits
Built with [Streamlit](https://streamlit.io/) and ❤️ by **Amin**
