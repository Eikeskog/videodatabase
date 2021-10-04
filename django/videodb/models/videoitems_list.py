from django.db import models
from django.utils import timezone
from .videoitem import Videoitem

class VideoitemsList(models.Model):
    class Meta:
        db_table = 'user_list'
        ordering = ['label']

    label = models.CharField(max_length=120)
    user_id = models.CharField(max_length=120, null=True, blank=True) # not implemented.
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    videoitems = models.ManyToManyField(to=Videoitem)
    items_count = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(VideoitemsList, self).save(*args, **kwargs)

    def __str__(self):
        return self.label
