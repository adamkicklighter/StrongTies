# StrongTies Installation Guide

Welcome to StrongTies! This guide will help you set up and run StrongTies on your local computer. No advanced technical skills are required — just follow the steps below.

---

## 1. Prerequisites

Before you begin, make sure you have:

- **A computer running Windows, macOS, or Linux**
- **Python 3.8 or newer**  
  If you don’t have Python installed, download it from [python.org](https://www.python.org/downloads/).

- **Git (optional, but recommended)**  
  Download from [git-scm.com](https://git-scm.com/downloads).

---

## 2. Clone or Download the Repository

**Option A: Using Git (Recommended)**

Open your terminal (Command Prompt on Windows, Terminal on macOS/Linux) and run:

```
git clone https://github.com/adamkicklighter/StrongTies.git
```

**Option B: Download ZIP**

1. Go to [StrongTies on GitHub](https://github.com/adamkicklighter/StrongTies)
2. Click the green **Code** button, then **Download ZIP**
3. Unzip the folder to a location you can find

---

## 3. Set Up a Python Environment

It’s best to use a virtual environment to keep things organized.

**Windows:**

```
cd StrongTies
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```
cd StrongTies
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Required Packages

With your virtual environment activated, install dependencies:

```
pip install -r requirements.txt
```

If you see an error about `requirements.txt` missing, install manually:

```
pip install streamlit pandas
```

---

## 5. Run StrongTies

Start the app with:

```
streamlit run app/app.py
```

Your browser will open to the StrongTies interface.

---

## 6. Upload Your Data

- Export your LinkedIn connections as CSV (see the in-app instructions or [User Guide](./user-guide.md))
- Upload your CSV file(s) in the app
- Select your identifier and click **Analyze Network**

---

## 7. Troubleshooting

- If you see errors about missing packages, run `pip install <package>`.
- If the app doesn’t open, check your Python version (`python --version`).
- For help, see the [README](./README.md) or [User Guide](./user-guide.md).

---

## 8. Notes & Work in Progress

- **Features like network graph visualization and advanced metrics are coming soon.**
- The app is under active development—check GitHub for updates.
- All processing happens locally; your data is never uploaded.

---

## 9. Need Help?

- Review the [User Guide](./user-guide.md)
- Open an issue on [GitHub](https://github.com/adamkicklighter/StrongTies/issues)
- Email: `strongties.networking@gmail.com`

---

*Thank you for supporting ethical, privacy-first networking!*