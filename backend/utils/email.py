import os
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
    if not user.receive_email:
        return 0

    name = user.real_name
    href = 'http://%s/event/%s' % (site_host, event.id)

    if approved:
        message = '您注册参加<a href="%s">%s</a>的申请已被管理员批准，活动将于%s在%s举行，请按时参加。'
        message %= (href, event.title, event.start_time, event.location)

        subject = '%s通知: 您参加%s的申请已被管理员批准' % (site_name, event.title)
    else:
        message = '您注册参加<a href="%s">%s</a>的申请未能通过管理员审核，感谢您的理解。'
        message %= (href, event.title)

        subject = '%s通知: 您参加%s的申请未通过审核' % (site_name, event.title)

    content = '<p>亲爱的 <strong>%s</strong> 您好:</p>\n' % name
    content += '<p>%s</p>\n' % message
    content += '<p> <a href="%s">%s</a> team</p>\n' % (site_host, site_name)

    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")

    return msg.send()


def send_registered_email(user, event, approved=True):
    if not user.receive_email:
        return 0

    name = user.real_name
    href = 'http://%s/event/%s' % (site_host, event.id)

    if approved:
        message = '您已成功注册<a href="%s">%s</a>，活动将于%s在%s举行，请按时参加。'
        message %= (href, event.title, event.start_time, event.location)

        subject = '%s通知: 您已成功注册%s' % (site_name, event.title)
    else:
        message = '您已申请注册<a href="%s">%s</a>，请等待管理员审核。'
        message %= (href, event.title)

        subject = '%s通知: 您已申请注册%s，等待管理员审核' % (site_name, event.title)

    content = '<p>亲爱的 <strong>%s</strong> 您好:</p>\n' % name
    content += '<p>%s</p>\n' % message
    content += '<p> <a href="%s">%s</a> team</p>\n' % (site_host, site_name)

    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")

    return msg.send()


def send_notification_email(ure, day_msg):
    '''
    @message '您注册的<a href="">event.title</a>将于（）后在event.location举行，请按时参加。'
    '''
    if not user.receive_email:
        return 0

    name = ure.user.real_name

    href = 'http://%s/event/%s' % (site_host, ure.event.id)
    message = '您注册的<a href="%s">%s</a>将于%s在%s举行，请按时参加。'
    message %= (href, ure.event.title, before_days[1], ure.event.location)

    subject = '%s提醒您: 您注册的%s将于%s开始' % (site_name, ure.event.title, day_msg)
    content = '<p>亲爱的 <strong>%s</strong> 您好:</p>\n' % name
    content += '<p>%s</p>\n' % message
    content += '<p> <a href="%s">%s</a> team</p>\n' % (site_host, site_name)

    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")

    return msg.send()
