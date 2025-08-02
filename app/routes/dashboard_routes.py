from flask import Blueprint, render_template, session, redirect, url_for, flash, request
import os
from app.models.applied_jobs import AppliedJobs
from app import db
from openai import OpenAI
from app.utils.location_resolver import resolve_location

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def dashboard_home():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', username=session.get('username'))

@dashboard.route('/search-by-cv', methods=['POST', 'GET'])
def cv_search_jobs():
    """Search jobs using extracted keywords from user's CV."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    from app.models.user import User
    from app.utils.cv_parser import extract_keywords_from_cv
    from app.utils.job_fetcher import fetch_jobs

    user = User.query.get(session['user_id'])

    if not user or not user.cv_filename:
        flash("Please upload your CV to search by skills.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    cv_path = os.path.join('app', 'static', 'uploads', user.cv_filename)
    if not os.path.exists(cv_path):
        flash("Uploaded CV not found. Please upload again.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    # Extract keywords and location
    result = extract_keywords_from_cv(cv_path)
    keywords = result.get("keywords", [])
    location = resolve_location(result.get("location", "").lower())

    if not keywords:
        flash("No useful keywords found in your CV. Try uploading a different file.", "warning")
        return redirect(url_for('dashboard.dashboard_home'))

    search_query = " ".join(keywords[:5])  # combine top 5 keywords

    # Pagination
    page = request.args.get('page', 1, type=int)
    jobs = fetch_jobs(keyword=search_query, location=location, job_type="", sort_by="relevant", page=page)

    # Save for reuse
    session['cv_search_query'] = search_query
    session['cv_search_location'] = location
    session['job_results'] = jobs
    session.modified = True

    print(f"📡 CV Search: '{search_query}' in {location} -> {len(jobs)} jobs fetched (Page {page})")

    # Calculate pagination dynamically
    total_jobs = 50 if len(jobs) == 10 else len(jobs)
    has_next = len(jobs) == 10

    return render_template('dashboard.html',
                           username=session.get('username'),
                           jobs=jobs,
                           total_count=total_jobs,
                           page=page,
                           has_next=has_next)


@dashboard.route('/search-jobs', methods=['POST', 'GET'])
def keyword_search_jobs():
    """Search jobs based on user-entered keyword and location."""
    if request.method == 'POST':
        session['keyword'] = request.form.get('keyword', '').strip()
        session['location'] = request.form.get('location', '').strip()
        session['job_type'] = request.form.get('job_type', '').strip()
        session['sort_by'] = request.form.get('sort_by', '').strip()
        page = 1
    else:
        page = request.args.get('page', 1, type=int)

    keyword = session.get('keyword', '')
    location = resolve_location(session.get('location', ''))
    job_type = session.get('job_type', '')
    sort_by = session.get('sort_by', '')

    from app.utils.job_fetcher import fetch_jobs
    jobs = fetch_jobs(keyword=keyword, location=location, job_type=job_type, sort_by=sort_by, page=page)

    # Save results in session
    session['job_results'] = jobs
    session.modified = True

    print(f"📡 Keyword Search: '{keyword}' in {location} -> {len(jobs)} jobs fetched (Page {page})")

    # Dynamic total count for pagination
    total_jobs = 50 if len(jobs) == 10 else len(jobs)
    has_next = len(jobs) == 10

    return render_template('dashboard.html',
                           username=session.get('username'),
                           jobs=jobs,
                           total_count=total_jobs,
                           page=page,
                           has_next=has_next)


@dashboard.route('/apply-job', methods=['POST'])
def apply_job():
    if 'user_id' not in session:
        flash("Please log in to apply.", "warning")
        return redirect(url_for('auth.login'))

    job_title = request.form.get('job_title')
    company = request.form.get('company')
    apply_link = request.form.get('apply_link')

    if not all([job_title, company, apply_link]):
        flash("Incomplete job details.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    applied = AppliedJobs(user_id=session['user_id'], job_title=job_title,
                          company=company, apply_link=apply_link, status='Applied')
    db.session.add(applied)
    db.session.commit()

    flash("Job successfully applied and recorded.", "success")
    return redirect(apply_link)

@dashboard.route('/prepare-cover-letter', methods=['POST'])
def prepare_cover_letter():
    print("🔁 Entered /prepare-cover-letter route")

    if 'job_results' not in session:
        flash("No job listings available to apply.", "warning")
        return redirect(url_for('dashboard.dashboard_home'))

    print("✅ job_results found:", len(session['job_results']))


    selected_indices = request.form.getlist("selected_jobs")
    if not selected_indices:
        flash("Please select at least one job to apply.", "warning")
        return redirect(url_for('dashboard.dashboard_home'))

    job_results = session['job_results']
    selected_jobs = []
    for index in selected_indices:
        try:
            job = job_results[int(index)]
            selected_jobs.append({
                "job_title": job.get("job_title", ""),
                "company": job.get("company") or job.get("employer_name", "Unknown"),
                "apply_link": job.get("apply_link", ""),
                "employer_name": job.get("employer_name", "Unknown")
            })
        except (IndexError, ValueError) as e:
            print("❌ Error parsing selected job index:", e)

    session['jobs_to_apply'] = selected_jobs
    session['current_job_index'] = 0
    return redirect(url_for('dashboard.cover_letter_review'))

@dashboard.route('/cover-letter-review', methods=['POST', 'GET'])
def cover_letter_review():
    from app.models.user import User
    from app.utils.cv_parser import extract_keywords_from_cv
    import openai, datetime

    if 'user_id' not in session:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user or not user.cv_filename:
        flash("Please upload your CV to apply for jobs.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    if request.method == 'POST':
        selected_indices = request.form.getlist('selected_jobs')
        job_results = session.get('job_results', [])
        jobs = []
        for index in selected_indices:
            try:
                job = job_results[int(index)]
                jobs.append({
                    "job_title": job.get("job_title", ""),
                    "company": job.get("company") or job.get("employer_name", "Unknown"),
                    "apply_link": job.get("apply_link", ""),
                    "employer_name": job.get("employer_name", "Unknown")
                })
            except Exception as e:
                print("Error parsing job from index:", e)
        if not jobs:
            flash("No valid jobs selected.", "warning")
            return redirect(url_for('dashboard.dashboard_home'))
        session['jobs_to_apply'] = jobs
        session['current_job_index'] = 0

    jobs = session.get('jobs_to_apply', [])
    index = session.get('current_job_index', 0)
    if index >= len(jobs):
        flash("All selected jobs have been processed.", "info")
        return redirect(url_for('dashboard.dashboard_home'))

    job = jobs[index]
    cv_path = os.path.join('app', 'static', 'uploads', user.cv_filename)
    parsed_cv = extract_keywords_from_cv(cv_path)

    user_name = parsed_cv.get('user_name', user.username)
    email = parsed_cv.get('email', user.email)
    phone = parsed_cv.get('phone', '')
    skills = ', '.join(parsed_cv['keywords'])

    openai.api_key = os.getenv("OpenAI_API_KEY")
    client = OpenAI(api_key=openai.api_key)

    prompt = f"""
    Write a professional cover letter for the position of {job['job_title']} at {job['company']}.
    Address the hiring manager. Use the following applicant details:
    - Name: {user_name}
    - Email: {email}
    - Phone: {phone}
    - Application Date: {datetime.datetime.now().strftime('%d %B %Y')}
    Mention these relevant skills from CV: {skills}.
    Keep the tone polite, confident, and job-specific.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    letter = response.choices[0].message.content

    return render_template("cover_letter_review.html", cover_letters=[{"job": job, "letter": letter}])

@dashboard.route('/submit-cover-letter', methods=['POST'])
def submit_cover_letter():
    from app.models.user import User
    from app.utils.email_utils import send_application_confirmation
    import datetime

    user = User.query.get(session.get('user_id'))
    job_list = session.get('jobs_to_apply', [])
    index = session.get('current_job_index', 0)

    if index >= len(job_list):
        flash("No more jobs to process.", "info")
        return redirect(url_for('dashboard.dashboard_home'))

    job = job_list[index]
    cover_letter = request.form.get('cover_letter', '')

    db.session.add(AppliedJobs(user_id=user.id, job_title=job["job_title"],
                               company=job["company"], apply_link=job["apply_link"],
                               status='Applied', timestamp=datetime.datetime.utcnow()))

    try:
        send_application_confirmation(user.email, job, cover_letter)
    except Exception as e:
        print("❌ Email send failed:", e)

    db.session.commit()
    session["current_job_index"] = index + 1
    return redirect(url_for('dashboard.cover_letter_review'))

# chatbot and resolve_cities remain unchanged

@dashboard.route('/chatbot', methods=['POST'])
def chatbot():
    from openai import OpenAI
    import os

    client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))

    user_message = request.form.get('message', '').strip()

    # ✅ Reject confidential questions politely
    restricted_keywords = ["password", "secret key", "database", "admin panel", "api key"]
    if any(word in user_message.lower() for word in restricted_keywords):
        return {"response": "I’m sorry, but I can’t help with confidential or sensitive information."}

    # ✅ Context about your app features
    system_prompt = """
    You are the AI Help Assistant for AI JobBot. 
    Only answer questions about this application and its features. 
    If the user says hello or hi, greet them politely.
    If the user asks anything unrelated to this app or outside the supported features, reply:
    'I’m here to help only with AI JobBot features such as registration, login, uploading CV, 
    searching jobs, applying jobs, generating cover letters, viewing applied jobs, and profile management.'
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {"response": reply}
    except Exception as e:
        print("Chatbot error:", str(e))
        return {"response": "Sorry, something went wrong."}


@dashboard.route('/resolve-cities')
def resolve_cities():
    import requests

    name_prefix = request.args.get('namePrefix', '')
    if not name_prefix:
        return []

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    params = {
        "namePrefix": name_prefix,
        "limit": "10",
        "types": "CITY"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["data"]
        else:
            return []
    except Exception as e:
        print("GeoDB error:", e)
        return []

@dashboard.route('/regenerate-cover-letter', methods=['POST'])
def regenerate_cover_letter():
    from openai import OpenAI
    import os

    feedback = request.form.get("feedback", "")
    future_pref = request.form.get("future", "false") == "true"

    job_list = session.get('jobs_to_apply', [])
    index = session.get('current_job_index', 0)
    if index >= len(job_list):
        return {"new_letter": "No job found to regenerate."}

    job = job_list[index]
    user_id = session.get('user_id')
    from app.models.user import User
    user = User.query.get(user_id)

    client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))

    prompt = f"""
    Regenerate the following cover letter for the role {job['job_title']} at {job['company']} 
    with the following user-requested changes: {feedback}.
    Keep it professional and concise.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    new_letter = response.choices[0].message.content

    # Save future preference
    if future_pref:
        session["future_feedback"] = feedback

    return {"new_letter": new_letter}

@dashboard.route('/enhance-cover-letter', methods=['POST'])
def enhance_cover_letter():
    from openai import OpenAI
    import os

    text = request.form.get("text", "")
    client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))

    prompt = f"Improve the following text to make it sound more professional and polished:\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    enhanced_text = response.choices[0].message.content

    return {"enhanced_text": enhanced_text}


@dashboard.route('/view-job/<int:index>')
def view_job(index):
    """View details of a specific job from session results."""
    jobs = session.get('job_results', [])
    if 0 <= index < len(jobs):
        job = jobs[index]
        return render_template('view_job.html', job=job)
    else:
        flash("Job not found", "warning")
        return redirect(url_for('dashboard.dashboard_home'))