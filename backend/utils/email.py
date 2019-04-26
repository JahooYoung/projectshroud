from django.conf import settings
from django.core.mail import EmailMultiAlternatives


site_name = settings.SITE_OFFICIAL_NAME
site_host = settings.SITE_HOST_NAME
site_domain = settings.SITE_DOMAIN_NAME
activate_url = settings.USER_ACTIVATE_URL


def send_activation_email(user):
    id = user.id
    name = user.real_name
    token = user.activate_token
    activation_link = 'http://%s%s?token=%s' % (site_host, activate_url, token)

    subject = '请激活您的%s账户' % site_name
    content = '<p>亲爱的 <strong>%s</strong> 您好:</p>\n' % name
    content += '<p>感谢您注册 <strong>%s</strong> 的账户，请点击以下链接验证您的邮箱并激活账户：</p>\n' % site_name
    content += '<p><a href="%s">激活账户</a> (如不成功请将链接复制到地址栏访问: %s)</p>\n' % (activation_link, activation_link)
    content += '<p> <a href="%s">%s</a> team</p>\n' % (site_host, site_name)

    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")

    return msg.send()


def send_approve_or_reject_email(user, event, approved=True):
    # Todo
    return True


def send_registered_email(user, event, approved=True):
    # Todo
    return True

