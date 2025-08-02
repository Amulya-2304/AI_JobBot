import docx2txt
import PyPDF2
import re

def extract_keywords_from_cv(cv_path):
    """Extract keywords, location, and user info from a CV (PDF/DOCX)."""
    text = ""

    if cv_path.endswith('.pdf'):
        with open(cv_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""

    elif cv_path.endswith('.docx'):
        text = docx2txt.process(cv_path)

    # Keep original text for address extraction (case-sensitive)
    original_text = text
    text = text.lower()

    # ✅ Whitelist for keyword extraction
    whitelist = [
        "python", "java", "sql", "flask", "django", "react", "html", "css", "javascript", "api",
        "machine learning", "deep learning", "ai", "data analysis", "data analytics", "cloud", "aws",
        "medical coder", "nurse", "doctor", "radiology", "pharmacist", "healthcare assistant",
        "sales", "marketing", "retail", "customer service", "cashier", "e-commerce", "telecalling",
        "civil engineer", "construction", "plumber", "electrician", "mechanic", "supervisor",
        "graphic designer", "ui/ux", "interior designer", "fashion designer", "photographer",
        "model", "actor", "actress", "editor", "video editing",
        "teacher", "tutor", "trainer", "content writer", "librarian",
        "cook", "chef", "cleaner", "maid", "babysitter", "housekeeper",
        "driver", "delivery", "warehouse", "packer", "logistics", "inventory",
        "admin", "accountant", "receptionist", "hr", "assistant", "executive",
    ]

    # 🔍 Extract keywords
    keywords = [word for word in whitelist if word in text]
    print("🔍 CV Scan Extracted Keywords:", keywords)

    # 🌍 Extract location
    location_matches = re.findall(
        r'\b(berlin|germany|hyderabad|bangalore|mumbai|india|usa|new york|remote|london|canada|paris|delhi)\b',
        text
    )
    location = location_matches[0] if location_matches else "remote"
    print("📍 Extracted Location from CV:", location)

    # 👤 Extract personal details
    name_match = re.search(r'name[:\-\s]*([A-Za-z ]+)', text)
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone_match = re.search(r'\+?\d[\d\s\-\(\)]{7,}', text)

    user_name = name_match.group(1).strip() if name_match else "Applicant"
    user_email = email_match.group(0) if email_match else ""
    user_phone = phone_match.group(0) if phone_match else ""

    # 🏠 Extract address (look for lines starting with 'address' or typical address patterns)
    address_match = re.search(r'(address[:\-\s]*)([A-Za-z0-9,\.\-\s]+)', original_text, re.IGNORECASE)
    user_address = address_match.group(2).strip() if address_match else ""
    # Fallback: look for a line with numbers and street/road/ave
    if not user_address:
        address_fallback = re.search(r'([0-9]{1,5} [A-Za-z0-9 ,\.-]+(Street|St\.|Road|Rd\.|Avenue|Ave\.|Lane|Ln\.|Blvd|Boulevard|Drive|Dr\.|Block|Sector)[A-Za-z0-9 ,\.-]*)', original_text, re.IGNORECASE)
        user_address = address_fallback.group(0).strip() if address_fallback else ""

    # 🔗 Extract GitHub and LinkedIn links
    github_match = re.search(r'(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+', original_text, re.IGNORECASE)
    linkedin_match = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+', original_text, re.IGNORECASE)
    github_url = github_match.group(0) if github_match else ""
    linkedin_url = linkedin_match.group(0) if linkedin_match else ""

    return {
        "keywords": keywords or ["job", "assistant"],
        "location": location,
        "user_name": user_name,
        "email": user_email,
        "phone": user_phone,
        "address": user_address,
        "github": github_url,
        "linkedin": linkedin_url
    }