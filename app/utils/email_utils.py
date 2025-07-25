from flask_mail import Message
from app import mail

def send_reset_email(to_email, link):
    msg = Message('Reset Your Password - AI JobBot',
                  recipients=[to_email],
                  sender='noreply@AIbot.com')
    msg.body = f'Click this link to reset your password:\n{link}\n\nIf not requested, ignore this.'
    mail.send(msg)


def send_application_confirmation(to_email, job, letter):
    """
    Send confirmation email after the job application.
    """
    msg = Message(
        subject=f"Application Submitted: {job['job_title']} at {job['company']}",
        recipients=[to_email],
        sender='noreply@AIbot.com'
    )
    msg.body = f"""
Hello,

You successfully applied for the position of {job['job_title']} at {job['company']}.

Application Link: {job['apply_link']}

📝 Cover Letter:
{letter}

Thank you for using AI JobBot.
"""
    mail.send(msg)