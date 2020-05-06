from django.db import models
import string
from random import randint, choice

# Create your models here.

def _generate(**kwargs):
    """Generate random string

    Returns:
        str -- generated random string
    """
    min_length = 16
    max_length = 32
    chars = string.ascii_letters + string.digits

    return "".join(choice(chars) for x in range(randint(min_length, max_length)))


class File(models.Model):
    """ Uploaded file with TTL """

    class Meta:
        ordering = ['name']

    original_name = models.CharField(max_length=250)
    name = models.CharField(max_length=32, default=_generate)
    file = models.FileField(upload_to='files', null=False)
    ttl = models.SmallIntegerField(default=300, null=False)
    comment = models.CharField(max_length=250)
    ts = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=128, null=False, blank=False)
    used = models.BooleanField(default=False)

    def get_absolute_link(self):
        return "/get/{}".format(self.name)