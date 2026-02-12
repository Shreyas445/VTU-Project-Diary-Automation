# VTU Project Diary Automation

This Python script automates the process of filling out the 18-week project diary on the VTU Internyet Portal. It uses Selenium WebDriver to log in, navigate the dashboard, and populate weekly entries from a JSON file.

## 🚀 Features

*   **Automated Login**: Securely logs in using credentials stored in a local JSON file.
*   **Batch Processing**: Automatically fills entries for all 18 weeks in one go.
*   **Smart Selection**: Handles dropdowns for Project, Year, and Month, and dynamically picks the correct Day from the calendar.
*   **Robust Form Filling**: Populates "Work Summaries", "Hours Worked", "Learnings/Outcomes", and handles multi-select "Skills Used".
*   **Error Handling**: Includes retry logic and fallback mechanisms for tricky web elements.

## 📋 Prerequisites

*   [Python 3.x](https://www.python.org/downloads/) installed on your system.
*   Google Chrome browser installed.
*   An active account on the [VTU Internyet Portal](https://vtu.internyet.in/).

## 🛠️ Installation

1.  **Clone this repository** (or download the files):
    ```bash
    git clone https://github.com/Shreyas445/VTU-Project-Diary-Automation
    
    ```

2.  **Install Dependencies**:
    Run the following command to install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

### 1. Credentials
Create a file named `credentials.json` in the same directory as the script. **Do not commit this file to GitHub.**

**`credentials.json`**:
```json
{
    "email": "YOUR_EMAIL",
    "password": "YOUR_PASSWORD"
}
```

### 2. Diary Entries
Edit the `project_diary_entries.json` file to include your specific weekly updates. Ensure the date format is `DD-MM-YYYY`.

**`project_diary_entries.json`** (Example):
```json
[
  {
    "week": 1,
    "date": "11-02-2025",
    "work_summary": "Literature survey and problem definition...",
    "hours_worked": 6.0,
    "learnings_outcomes": "Understood the core requirements...",
    "skills_used": ["Python", "Research"]
  },
  ...
]
```

## 📝 Generating Entries with AI

Don't want to type your entries manually? Since you likely already have a `Project Logbook` (PDF), you can use an AI chatbot (like ChatGPT, Gemini, or Claude) to convert it into the required JSON format.

1.  **Upload your Project Logbook PDF** to the AI.
2.  **Copy and Paste the following prompt** to generate the `project_diary_entries.json` content:

```text
You are an AI system that extracts structured project diary data from a VTU logbook PDF.

TASK:
Convert the uploaded Project Logbook PDF into a structured JSON format suitable for automatic entry in the VTU Project Diary Portal.

IMPORTANT RULES:

1. Extract only WEEK-WISE meeting entries.
2. Ignore:
   - Cover pages
   - Certificates
   - Declarations
   - Student calendar
   - Tables not related to weekly reports

3. Extract from each week:
   - Week number
   - Date
   - Work done / Discussion Points
   - Findings / Outcomes

4. STRICT OUTPUT RULE:
   - Generate EXACTLY 18 structured entries.
   - The 18 entries must represent the COMPLETE project lifecycle.
   - Always include:
       • Initial planning phase
       • Design phase
       • Implementation phase
       • Testing phase
       • Documentation phase
       • Final review / demonstration / completion
   - If the logbook contains MORE than 18 weeks:
       → Intelligently merge closely related intermediate weeks.
       → Preserve chronological order.
       → Ensure final completion week is included.
   - If the logbook contains LESS than 18 weeks:
       → Split detailed weeks logically to reach 18 entries.
   - Never cut off before project completion.

5. Maintain chronological order by date.

6. Continue sequential numbering from 1 to 18.

7. Ensure no duplicate dates.
   - If merging weeks, use the later date of the merged entries.

8. Map fields to VTU portal format:

   "week": Sequential number (1–18)
   "date": Date in DD-MM-YYYY format
   "work_summary": Professional 1–2 sentence summary derived from "Work done / Discussion Points"
   "hours_worked": Always assign 6.0 unless explicitly specified otherwise
   "learnings_outcomes": Academic learning statement derived from "Findings / Outcomes"
   "skills_used": Select ONLY from the allowed skills list

9. Allowed Skills List (STRICT SELECTION ONLY):
   [
     C++, Circuit Design, IoT, Kotlin, AWS, Azure, Computer vision, Canva, DevOps, CSS, 
     Data modeling, Embedded Systems, Java, JavaScript, Data Encryption, Flutter, Git, 
     Docker, firewall configuration, HTML, Kubernets, Layout Design, Machine Learning, 
     Google Cloud, PostgreSql, mySql, Node.js, React.js, PHP, Python, VLSI Design
   ]

   Do NOT invent new skills. Select skills logically based on work performed.

10. Maintain professional academic tone throughout.

11. Output requirements:
   - STRICT JSON array only
   - No explanation
   - No markdown
   - No comments
   - Only valid JSON

OUTPUT FORMAT:

[
  {
    "week": 1,
    "date": "DD-MM-YYYY",
    "work_summary": "...",
    "hours_worked": 6.0,
    "learnings_outcomes": "...",
    "skills_used": ["IoT", "Embedded Systems"]
  }
]

Now analyze the uploaded logbook PDF and generate exactly 18 structured entries that represent the complete project lifecycle from start to final completion.
```

3.  **Copy the JSON output** from the AI and save it as `project_diary_entries.json` in the project folder.

## ▶️ Usage

1.  Make sure you have your `credentials.json` and `project_diary_entries.json` ready.
2.  Run the script:
    ```bash
    python fill_diary.py
    ```
3.  The browser will open and perform the following actions:
    *   Log in to the portal.
    *   Navigate to the Project Diary section.
    *   Loop through each week in your JSON file, filling out the details and saving the entry.
4.  Once finished, the terminal will prompt you to press **Enter** to close the browser.

## ⚠️ Important Notes

*   **XPaths**: This script uses specific XPaths for the VTU portal elements. If the portal's design changes, these XPaths in `fill_diary.py` might need updating.
*   **Execution Speed**: `time.sleep()` delays are added to ensure the website processes clicks and animations. Do not remove them, or the script might fail.
*   **Browser Window**: Do not minimize the browser window while the script is running, as some elements require focus to be interacted with.

## 👨‍💻 Developer

Developed by **Shreyas**
- **GitHub**: [https://github.com/Shreyas445](https://github.com/Shreyas445)
- **Repo**: [https://github.com/Shreyas445/VTU-Internship-Diary-Automation](https://github.com/Shreyas445/VTU-Internship-Diary-Automation)

## 🤝 Contributing

Feel free to fork this project and submit pull requests if you find better ways to handle valid element selection or optimize the flow!

## 📜 Disclaimer & Terms of Use

**Please read this section carefully before using the software.**

### 1. No Responsibility
This software is provided "as is" without any guarantees or warranty. In association with the product, the developer (**Shreyas445**) makes no warranties of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, of title, or of non-infringement of third-party rights. Use of the software by a user is at the user’s risk.

**The developer is NOT responsible for:**
*   Any academic penalties, rejections, or disciplinary actions faced by the user.
*   Data loss, account bans, or technical issues on the VTU portal.
*   Misuse of this tool for spamming or malicious activities.
*   Any "bad things" that happen as a result of using this automation script.

### 2. Educational Purpose Only
This tool is intended solely for **educational purposes** to demonstrate Python Selenium automation capabilities. It is not intended to bypass any security measures or violate the terms of service of the VTU Internship Portal. Users are responsible for ensuring their use of this tool complies with all relevant university regulations and laws.

### 3. Privacy Policy
*   **Local Execution**: This script runs entirely on your local machine.
*   **No Data Collection**: The developer does **not** collect, store, or transmit any of your personal data, login credentials (`credentials.json`), or diary entries.
*   **Credentials Security**: Your `credentials.json` file remains on your computer. You are responsible for keeping this file secure and not sharing it publicly (e.g., do not commit it to GitHub).

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

