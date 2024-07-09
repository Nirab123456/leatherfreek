from django.core.mail import send_mail , get_connection
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from decouple import config


def contact_form_recived_mail(email, name, message):
    try:
        my_host = config('EMAIL_HOST')
        my_port = config('EMAIL_PORT', cast=int)
        my_username = config('SUPPORT_EMAIL')
        my_password = config('EMAIL_HOST_PASSWORD')
        my_use_tls = True
        my_use_ssl = False
        my_from_email = config('SUPPORT_EMAIL')
        my_recipient_list = [email]
        my_subject = f'New contact form submission from {name}'
        my_message = message
        my_html_message = render_to_string('auto_emails/about_contact_auto_email.html')
        my_fail_silently = False
        my_connection = get_connection(
            host=my_host,
            port=my_port,
            username=my_username,
            password=my_password,
            use_tls=my_use_tls,
            use_ssl=my_use_ssl,
        )
        send_mail(
            subject=my_subject,
            message=my_message,
            from_email=my_from_email,
            recipient_list=my_recipient_list,
            html_message=my_html_message,
            fail_silently=my_fail_silently,
            connection=my_connection,
        )

    except ValidationError as e:
        # Handle validation errors (if any)
        print(f"Validation error occurred: {e}")


