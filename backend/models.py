import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model


def generate_user_uuid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))[0:16]


def generate_event_uuid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))[0:12]


def generate_checkin_uuid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))[0:10]


class UserProfileManager(BaseUserManager):
    def create_user(self, mobile, real_name, email, password=None):
        """
        Creates and saves a User with the given email, real name,
        email and password.
        """
        if not mobile:
            raise ValueError('Users must have a mobile number')

        if not real_name:
            raise ValueError('Users must have a real name')

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
        )
        user.is_site_admin = True
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
    email = models.EmailField('电子邮件', blank=True)
    date_joined = models.DateField('注册时间', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_site_admin = models.BooleanField(default=False)
    # IDtype, ID number, ProfileImage

    USERNAME_FIELD = 'mobile'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['real_name', 'email']

    objects = UserProfileManager()

    def __str__(self):
        return self.real_name

    def has_perm(self, perm, obj=None):
        return self.is_site_admin

    def has_module_perms(self, app_label):
        return self.is_site_admin

    @property
    def is_staff(self):
        return self.is_site_admin


class Event(models.Model):
    id = models.CharField(max_length=12,
        primary_key=True,
        default=generate_event_uuid,
        editable=False
    )
    title = models.CharField(max_length=50, blank=False, default='', verbose_name='活动名称')
    description = models.TextField('描述', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    location = models.CharField(max_length=50, blank=False)
    host = models.ForeignKey(get_user_model(), related_name='event_host', on_delete=models.CASCADE, verbose_name='创建者')
    admins = models.ManyToManyField(get_user_model(), through='UserManageEvent', related_name='admins')
    registered_attendee = models.ManyToManyField(get_user_model(), through='UserRegisterEvent', related_name='registered_attendee')
    public = models.BooleanField('是否公开', default=True)
    require_approve = models.BooleanField('注册需要审核', default=False)
    checkin_enabled = models.BooleanField('正在签到', default=False)

    class Meta:
        ordering = ('create_time',)

    def __str__(self):
        return self.title

    @property
    def host_display_info(self):
        return self.host.real_name

    def enable_checkin(self):
        self.checkin_enabled = True

    def disable_checkin(self):
        self.checkin_enabled = False

    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = 'table' if self.linenos else False
    #     options = {'title': self.title} if self.title else {}
    #     formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                             full=True, **options)
    #     self.highlighted = highlight(self.code, lexer, formatter)
    #     super(Snippet, self).save(*args, **kwargs)


class CheckIn(models.Model):
    token = models.CharField(max_length=10,
        primary_key=True,
        default=generate_checkin_uuid,
        editable=False
    )
    event = models.OneToOneField(Event, on_delete=models.CASCADE)


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
    other_detail = models.TextField('详细信息', blank=True)

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
    checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return '人员: %s, 活动: %s, 交通信息: %s' % (self.user, self.event, self.transport)

    def checkin(self):
        self.checked_in = True


class UserManageEvent(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return '管理员: %s, 活动: %s' % (self.user, self.event)

