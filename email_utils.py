import requests
from flask import current_app

def send_email(to, subject, text):
    """
    Envia e-mail via Mailgun ou SendGrid usando requests.
    """
    try:
        response = requests.post(
            current_app.config['API_URL'],
            auth=("api", current_app.config['API_KEY']),
            data={
                "from": current_app.config['API_FROM'],
                "to": to if isinstance(to, list) else [to],
                "subject": f"{current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}",
                "text": text
            }
        )
        print("E-mail enviado:", response.status_code, response.text)
        return response
    except Exception as e:
        print("Erro no envio:", e)
        return None
