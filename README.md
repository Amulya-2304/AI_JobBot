# 🤖 AI Job Application Bot

Welcome to the **AI Job Application Bot** is an advanced **AI-powered, full-stack job search assistant** that automates and enhances the job hunting process using **NLP, Machine Learning, LLMs (GPT-4o), and intelligent automation**.

This platform empowers job seekers to **search, apply, and track job applications** seamlessly — making the entire process **smarter, faster, and more efficient**.

---

## 🚀 Overview

Finding and applying for jobs can be tedious. AI Job Application Bot simplifies this process by:
- Fetching **real-time job listings** from multiple sources like LinkedIn, Glassdoor, StepStone, Google Jobs, and more.
- Using **Natural Language Processing (NLP)** to scan and parse resumes automatically.
- Generating **personalized, professional cover letters** with OpenAI's GPT-4o.
- Allowing **one-click job applications** with email confirmations and status tracking.
- Providing an **AI-powered chatbot assistant** to help with platform navigation and career guidance.


---

### 🛠️ Tech Stack

### **Frontend**
- HTML5, CSS3 (Vanilla)
- Jinja2 Templates (via Flask)
- JavaScript (Dynamic chatbot UI & AJAX requests)

### **Backend**
- Python 3.13
- Flask 2.3.3 (Blueprint-based modular structure)
- SQLAlchemy ORM with SQLite database
- Flask-Mail (Gmail SMTP integration)
- Flask-Session (Server-side sessions)

### **AI & NLP**
- OpenAI GPT-4o: For **cover letter generation** and **chatbot assistant**
- NLP Resume Parser: Extracts **skills, contact info, and job keywords** from PDF/DOCX
- AI-enhanced cover letter rewriting and text polishing

### **APIs**
- **RapidAPI**:
  - JSearch API (LinkedIn, Glassdoor, StepStone, Google Jobs)
  - GeoDB Cities API (Location auto-suggestions)
- **Fallback API**: Adzuna for European job listings when JSearch returns incomplete data
- **Email API**: Gmail SMTP with App Password.

---

## 🌟 Key Features

### 🧾 **Secure Authentication**
- User registration and login
- Forgot password flow with secure reset link
- Session-based user management

### 📄 **CV Upload & Smart Parsing**
- Supports **PDF/DOCX resumes**
- AI-powered extraction of:
  - Name, Email, Phone
  - Skills & Keywords
  - Location
- **Skip option** for first-time users

### 🔍 **Job Search**
- Search by:
  - **Keywords** (title, skills, company)
  - **Scanned CV** (auto-match to skills)
- Smart Filters:
  - Location with **auto-suggest dropdown**
  - Job type: Full-time, Part-time, Remote, WFH
  - Sort by: Relevant, Last 24 hours, Last 7 days
- **Multi-page results:** Up to 100 jobs (10 per page)

### ✅ **Automated Job Applications**
- Select multiple jobs or apply to all
- AI generates **unique cover letter per job**
- Allows:
  - Manual editing of cover letters
  - AI-enhanced rewriting suggestions
  - Feedback-based regeneration
- Sends **confirmation email** after applying
- Tracks application status: Applied, Pending, Reviewed, Rejected

### 📁 **Profile Management**
- View username, email, and masked password
- Upload/View/Delete CV anytime
- View all applied jobs with their current status

### 💬 **AI Chatbot Assistant**
- Powered by GPT-4o
- Answers **only job-bot-related queries** (secure, ignores confidential data)
- Helps users navigate the app, improve CVs, and get job search tips

----
## ⚡ Future Enhancements

- **Advanced ATS Optimization:** CV scoring and ATS compatibility analysis for better recruiter visibility.  
- **Job Recommendation Engine:** AI-driven recommendations tailored to candidate profiles.  
- **More APIs:** Adding Indeed, ZipRecruiter, and other global job sources.  
- **Improved Cover Letter Personalization:** Extracting recruiter details for even more targeted letters.  
- **One-click Auto-Apply Mode:** AI scans and applies to relevant jobs autonomously

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