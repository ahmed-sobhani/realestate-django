from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(
        email_type="pass_reset",
        subject=None,
        email_to=None,
        email_from=settings.CONTACT_EMAIL,
        context=dict(),
        headers=dict(),
):
    if email_type == "pass_reset":
        html_file = "emails/pass_reset.html"

    context['contact_email'] = settings.CONTACT_EMAIL
    context['contact_phone'] = settings.CONTACT_PHONE

    html_content = render_to_string(html_file, context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject, text_content, email_from, [email_to], headers=headers
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
