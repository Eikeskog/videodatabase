from django.db import models
import uuid


class VideoitemIssue(models.Model):
    class Meta:
        db_table = "videoitem_issue"

    issue_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    missing_file_db_fullpath = models.CharField(max_length=255, null=True, blank=True)
    missing_file_last_writetime = models.DateTimeField(null=True, blank=True)
    missing_file_project_id = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=255, null=True, blank=True)

    located_fullpath = models.CharField(max_length=255, null=True, blank=True)
    located_datetime = models.DateTimeField(null=True, blank=True)

    videoitem = models.OneToOneField(to="Videoitem", on_delete=models.CASCADE)

    file_size = models.BigIntegerField(null=True, blank=True)
    file_last_modified = models.DateTimeField(null=True, blank=True)

    issue_opened_datetime = models.DateTimeField(null=True, blank=True)
    issue_is_resolved_status = models.BooleanField(default=False)
    issue_is_pending_status = models.BooleanField(default=False)
    issue_is_important = models.BooleanField(default=False)
    issue_is_silenced = models.BooleanField(default=False)
    issue_is_paused = models.BooleanField(default=False)

    duplicate_exist_in_db = models.BooleanField(default=False)
    duplicate_is_located_status = models.BooleanField(default=False)
    duplicate_is_located_datetime = models.DateTimeField()
    duplicate_is_located_on_same_disk = models.BooleanField(default=False)

    last_search_for_file_datetime = models.DateTimeField()

    local_disks_search_log_json = models.JSONField(null=True, blank=True)

    user_specified_moved_to_disk = models.CharField(max_length=120)
    user_specified_moved_disk_last_checked = models.DateTimeField()
    user_specified_file_deleted = models.BooleanField(default=False)

    hide_file_from_main_items = models.BooleanField(default=False)

    remove_item_completely_from_db = models.BooleanField(default=False)

    def __str__(self):
        return self.missing_file_db_fullpath
