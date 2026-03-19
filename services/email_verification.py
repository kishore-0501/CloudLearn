# services/email_verification.py
allowed_domains = ["ncirl.ie", "ucd.ie", "tcd.ie", "griffith.ie"]

def verify_email_domain(email):
    domain = email.split("@")[-1]
    return domain in allowed_domains