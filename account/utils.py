# account/utils.py

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib.auth.models import Permission
from account.permission_config import PERMISSION_CONFIG
from django.contrib.contenttypes.models import ContentType
def send_activation_email(user, activation_url):
    print("--- CHECKPOINT 6: send_activation_email function CALLED ---", flush=True)
    
    mail_subject = 'Activate your account'
    context = {
        'user': user,
        'activation_url': activation_url,
    }
    
    try:
        message = render_to_string('account/activation_email.html', context)
        print("--- CHECKPOINT 7: Email template rendered ---", flush=True)
        
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html"
        email.send()
        
        print("--- CHECKPOINT 8: email.send() command EXECUTED ---", flush=True)

    except Exception as e:
        print(f"--- ERROR in send_activation_email: {e} ---")


def send_reset_password_email(user, absolute_reset_url):
    print("--- CHECKPOINT 6: send_activation_email function CALLED ---", flush=True)
    
    mail_subject = 'Reset your Password'
    context = {
        'user': user,
        'reset_url': absolute_reset_url,
    }
    
    try:
        message = render_to_string('account/reset_password_email.html', context)
        print("--- CHECKPOINT 7: Email template rendered ---", flush=True)
        
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html"
        email.send()
        
        print("--- CHECKPOINT 8: email.send() command EXECUTED ---", flush=True)

    except Exception as e:
        print(f"--- ERROR in send_activation_email: {e} ---")


def assign_permission(user,role):
    role_permission=PERMISSION_CONFIG.get(role,{})
    for model,permissions in role_permission.items():
        content_type=ContentType.objects.get_for_model(model)
        for perm_codename in permissions:
            permission= Permission.objects.get(
                content_type=content_type,
                codename=f"{perm_codename}_{model._meta.model_name}"
            )
            user.user_permissions.add(permission)

# def assign_permission(user,role):
#     if user.is_customer:
#         return PERMISSION_CONFIG["customer"]
#     elif user.is_seller:
#         return PERMISSION_CONFIG["seller"]
#     return []
