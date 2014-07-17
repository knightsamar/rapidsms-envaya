from django.db import models
from django.db.models import Q
import datetime

class EnqueuedMessage(models.Model):
    STATUS_CHOICES = (
            ('q', 'Queued for delivery'),
            ('s', 'Successfully sent'),
            ('x', 'Error while sending'),
            )
    msg_id  = models.CharField(max_length=32, null=False, blank=False, primary_key=True)
    sent_at = models.DateField(auto_now=True, db_index=True)
    message = models.TextField()
    recipient = models.CharField(db_index=True, max_length=255) # not using contacts so we can query the field
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='q')

    @classmethod
    def messages_for(cls, country_code, max_delay):
        if max_delay is not None:
            messages = cls.objects.filter(Q(recipient__startswith=country_code)|Q(sent_at__lt=(datetime.datetime.now() - datetime.timedelta(seconds=max_delay))))
        else:
            messages = cls.objects.filter(recipient__startswith=country_code)
        return messages
