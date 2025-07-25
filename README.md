# 🤖 AI Job Application Bot

Welcome to the **AI Job Application Bot** — a full-stack AI-powered platform that transforms the job search process using intelligent automation, NLP, ML, LLM's and OpenAI.

Whether you're actively job hunting or casually browsing, this platform helps you:
- Search jobs from LinkedIn, Glassdoor, Google Jobs, and more
- Auto-generate personalized cover letters with AI
- Apply to jobs with one click
- Track application status
- Chat with a helpful AI assistant
- And much more...

---

## 🛠️ Tech Stack

**Frontend**
- HTML, CSS (Vanilla)
- Jinja2 (via Flask)
- JavaScript for chatbot integration

**Backend**
- Python 3.13
- Flask + Flask Blueprints
- SQLAlchemy (SQLite)
- Flask-Mail (Gmail SMTP)
- OpenAI GPT-4o for cover letter + chatbot
- Flask-Session for server-side sessions

**APIs Used**
- RapidAPI: JSearch / GeoDB Cities API
- OpenAI: ChatGPT API (GPT-4o)
- Google, LinkedIn, StepStone (via JSearch)
- Email: Gmail SMTP (App Password)

---

## 🌟 Key Features

### 🧾 User Authentication
- Register/Login with email
- Forgot Password via Email
- Secure session management

### 📤 Resume Upload & Parsing
- Upload CV (PDF or DOCX)
- Extract name, email, phone, location, and keywords using NLP
- Skip option for first-time users

### 🔍 Job Search
- Search via Keyword or Scanned CV
- Filters:
  - Location (auto-suggest via GeoDB)
  - Job Type: Full-time, Part-time, Remote, WFH
  - Sort By: Most Relevant, 24hr, 7 days
- Paginated Results (10 per page)

### ✅ Apply to Jobs
- Select jobs or apply to all
- Auto-generates **1 cover letter per job**
  - Extracts info from job + parsed CV
  - Allows editing the letter before submission
- Sends confirmation emails
- Stores job status: Applied, Rejected, Reviewed, Pending

### 📁 Profile Page
- View username and email
- Masked password (show/reset supported)
- Upload/Delete/View CV
- View previously applied jobs with status

### 💬 AI Chatbot (OpenAI)
- Chatbot integrated in dashboard
- Ask anything about the platform, resume tips, or AI help
- Powered by GPT-4o with helpful prompt context


###
For support or feedback, contact:

📨 Email: aijobbot.project@gmail.com
###
🌐 Website: Coming soon......
---

## ✨ Getting Started

### ✅ 1. Requests for pulling this Repository
```bash
git clone: 
- https://github.com/Amulya-2304/AI_JobBot.git
cd ai-job-bot