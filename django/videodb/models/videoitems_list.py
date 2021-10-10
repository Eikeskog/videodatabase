from django.db import models
from django.utils import timezone
from .videoitem import Videoitem


class VideoitemsList(models.Model):
    class Meta:
        db_table = "user_list"
        ordering = ["label"]

    label = models.CharField(max_length=120)
    user_id = models.CharField(max_length=120, null=True, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        to="core_user.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    videoitems = models.ManyToManyField(to=Videoitem)
    items_count = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(VideoitemsList, self).save(*args, **kwargs)

    def __str__(self):
        return self.label
