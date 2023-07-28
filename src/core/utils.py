import os

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def send_email(subject, html_content, to_email, to_name):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": os.environ.get("SENDER_NAME"), "email": os.environ.get("SENDER_EMAIL")}
    to = [{"email": to_email, "name": to_name}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
