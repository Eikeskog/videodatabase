from django.db import models


class Project(models.Model):
    class Meta:
        db_table = "project"
        ordering = ["name"]

    project_id = models.CharField(max_length=16, primary_key=True)

    name = models.CharField(max_length=120)
    displayname = models.CharField(max_length=120, default="", blank=True)

    creation_year = models.IntegerField(null=True, blank=True)

    newest_file = models.DateTimeField(null=True, blank=True)
    oldest_file = models.DateTimeField(null=True, blank=True)

    total_size_byte = models.BigIntegerField(null=True, blank=True)
    total_items_count = models.IntegerField(null=True, blank=True)
    total_duration_sec = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.project_id
