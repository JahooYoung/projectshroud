from backend.utils.uuid import *
from backend.utils.email import send_approve_or_reject_email, send_event_change_email
from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
import os


class UserProfileManager(BaseUserManager):
    def create_user(self, mobile, real_name, email, password=None, is_su=False):
        """
        Creates and saves a User with the given email, real name,
        email and password.
        """
        if not mobile:
            raise ValueError('User must have a mobile number')

        if not real_name:
            raise ValueError('User must have a real name')

        if not email:
            raise ValueError('User must have a valid email')

        user = self.model(
            mobile=mobile,
            email=self.normalize_email(email),
            real_name=real_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, real_name, email, password):
        """
        Creates and saves a superuser with the given mobile, real name,
        email and password.
        """
        user = self.create_user(
            mobile=mobile,
            email=email,
            real_name=real_name,
            password=password,
            is_su=True
        )
        user.is_site_admin = True
        user.activate()
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=16,
        primary_key=True,
        default=generate_user_uuid,
        editable=False
    )
    mobile = models.CharField(max_length=11, blank=False, verbose_name='手机号码', unique=True)
    real_name = models.CharField(max_length=20, blank=False, verbose_name='真实姓名')
    email = models.EmailField('电子邮件', blank=False, unique=True)
    date_joined = models.DateField('注册时间', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_site_admin = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)

    # profile_image = models.ImageField(
    #                         upload_to=os.path.join(FILE_ROOT, 'avatar'),
    #                         default=os.path.join(FILE_ROOT, 'avatar/default.png'),
    #                         height_field=100, width_field=100
    #                    )
    # IDtype, ID number

    activate_token = models.CharField(max_length=32, default=generate_uuid)
    receive_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'mobile'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['real_name', 'email']

    objects = UserProfileManager()

    def __str__(self):
        return self.real_name

    def has_perm(self, perm, obj=None):
        if not self.is_active:
            return False
        if obj is None:
            return self.is_site_admin
        if isinstance(obj, Event):
            return (obj.host == self or
                    UserManageEvent.objects.filter(user=self, event=obj).exists())
        if hasattr(obj, 'user'):
            return obj.user == self
        return False

    def has_module_perms(self, app_label):
        return self.is_staff

    def activate(self):
        self.is_activated = True
        self.generate_uuid = ''
        self.save()

    def generate_activate_token(self):
        self.activate_token = generate_uuid()
        self.save()

    @property
    def is_staff(self):
        return bool(self.is_site_admin and self.is_active)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(UserProfile, self).save(*args, **kwargs)
        else:
            old = UserProfile.objects.get(id=self.pk)
            if getattr(self, 'email', None) != getattr(old, 'email', None):
                self.is_activated = False
            super(UserProfile, self).save(*args, **kwargs)


class Event(models.Model):
    id = models.CharField(max_length=12,
        primary_key=True,
        default=generate_event_uuid,
        editable=False
    )
    title = models.CharField(max_length=50, blank=False, default='', verbose_name='活动名称')
    description = models.TextField('描述', blank=True)
    description_html = models.TextField(blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    start_time = models.DateTimeField('开始时间', db_index=True)
    end_time = models.DateTimeField('结束时间', db_index=True)
    location = models.CharField(max_length=50, blank=False)
    host = models.ForeignKey(get_user_model(), related_name='event_host', on_delete=models.CASCADE, verbose_name='创建者')
    admins = models.ManyToManyField(get_user_model(), through='UserManageEvent', related_name='admins')
    registered_attendee = models.ManyToManyField(get_user_model(), through='UserRegisterEvent', related_name='registered_attendee')
    public = models.BooleanField('是否公开', default=True)
    require_approve = models.BooleanField('注册需要审核', default=False)
    require_application = models.BooleanField('需要填写申请信息', default=False)
    require_attachment = models.BooleanField('需要提交申请文件', default=False)
    attendee_count = models.IntegerField(default=0)
    applicant_count = models.IntegerField(default=0)
    # checkin_enabled = models.BooleanField('正在签到', default=False)

    class Meta:
        ordering = ('create_time',)

    def __str__(self):
        return self.title

    @property
    def host_display_info(self):
        return self.host.real_name

    def newregistration(self):
        if self.require_approve:
            self.applicant_count += 1
        else:
            self.attendee_count += 1
        self.save()

    def newapproved(self):
        self.applicant_count -= 1
        self.attendee_count += 1
        self.save()

    def newunregistration(self, approved):
        if not approved:
            self.applicant_count -= 1
        else:
            self.attendee_count -= 1
        self.save()

    # def enable_checkin(self):
    #     self.checkin_enabled = True

    # def disable_checkin(self):
    #     self.checkin_enabled = False

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Event, self).save(*args, **kwargs)
        else:
            old = Event.objects.get(id=self.pk)
            important_change = False
            for field in ['start_time', 'end_time', 'location']:
                if getattr(self, field, None) != getattr(old, field, None):
                    important_change = True
            if important_change:
                send_event_change_email(self)
            super(Event, self).save(*args, **kwargs)


class CheckIn(models.Model):
    token = models.CharField(max_length=10,
        primary_key=True,
        default=generate_checkin_uuid,
        editable=False
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False)
    started = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

    def toggle(self):
        self.started = not self.started

    def newcheckin(self):
        self.count += 1
        self.save()


class Transport(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id = models.CharField(max_length=16,
        primary_key=True,
        default=generate_user_uuid,
        editable=False
    )
    type_choices = (
        ('Flight', '航班'),
        ('Train', '列车'),
        ('Other', '其他'),
    )
    transport_type = models.CharField(max_length=10, choices=type_choices)
    transport_id = models.CharField(max_length=10, blank=False, verbose_name='航班/列车号')
    depart_station = models.CharField(max_length=20, blank=True, verbose_name='出发站')
    depart_time = models.DateTimeField('出发时间', blank=True)
    arrival_station = models.CharField(max_length=20, blank=True, verbose_name='到达站')
    arrival_time = models.DateTimeField('到达时间', blank=False)
    accommodation = models.CharField(max_length=50, blank=True)
    other_detail = models.TextField('详细信息', blank=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        if self.transport_type == 'Flight':
            return '航班: %s' % self.transport_id
        elif self.transport_type == 'Train':
            return '车次: %s' % self.transport_id
        elif self.transport_type == 'Other':
            return '其他: %s %s' % (self.transport_id, self.other_detail)


class UserRegisterEvent(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, blank=True, null=True, on_delete=models.SET_NULL)
    date_registered = models.DateTimeField('注册时间', auto_now_add=True)
    date_approved = models.DateTimeField('批准时间', null=True)
    checked_in = models.BooleanField(default=False)

    application_text = models.TextField(default='')
    # attachment = models.FileField(
    #                         max_length=None,
    #                         upload_to='user',
    #                     )
    approved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_registration'),
        ]

    def __str__(self):
        return '人员: %s, 活动: %s, 交通信息: %s' % (self.user, self.event, self.transport)

    def checkin(self):
        self.checked_in = True

    def approve(self):
        self.approved = True
        self.save()
        send_approve_or_reject_email(self.user, self.event)

    def reject(self):
        if self.approved:
            raise ValidationError('Cannot reject an already approved event registration.')
        send_approve_or_reject_email(self.user, self.event, approved=False)

    @property
    def is_admin(self):
        return UserManageEvent.objects.filter(user=self.user, event=self.event).exists()


class UserManageEvent(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_registration'),
        ]

    def __str__(self):
        return '管理员: %s, 活动: %s' % (self.user, self.event)


class UserCheckIn(models.Model):
    ure = models.ForeignKey(UserRegisterEvent, on_delete=models.CASCADE)
    checkin = models.ForeignKey(CheckIn, on_delete=models.CASCADE)
