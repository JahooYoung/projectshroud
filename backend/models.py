from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    host = models.ForeignKey('auth.User', related_name='events', on_delete=models.CASCADE)

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