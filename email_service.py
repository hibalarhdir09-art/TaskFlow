
import requests

API_BASE = "https://personne2-task-functions-gxayfpbkgyfwcedg.belgiumcentral-01.azurewebsites.net/api"
API_KEY  = "g3xvSGpj6sQ52Xb9GoY8jA8mDAtZpyLC2aiFhRK2ju8tAzFuDp4pbA=="


def send_email(receiver_email, subject, message_content):
    try:
        response = requests.post(
            f"{API_BASE}/send-email",
            params={"code": API_KEY},
            json={
                "toEmail": receiver_email,
                "subject": subject,
                "message": message_content
            }
        )
        result = response.json()
        print("Email sent successfully!")
        print("Result:", result)
        return True
    except Exception as error:
        print("Email sending failed:", error)
        return False