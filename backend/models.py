from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11, blank=False)
    real_name = models.CharField(max_length=20, blank=False)
    # IDtype, ID number, ProfileImage


class Transport(models.Model):
    # Todo
    pass


class Event(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    host = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    registered_attendee = models.ManyToManyField(User, through='UserRegisterEvent')

    class Meta:
        ordering = ('create_time',)

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


class UserRegisterEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_transport = models.ForeignKey(Transport, blank=True, null=True, on_delete=models.SET_NULL)
    date_registered = models.DateTimeField()
