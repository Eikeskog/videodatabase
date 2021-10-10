from django.db.models.expressions import F
from django.db import models
from .project import Project
from ..utils.functions.common import (
    disk_from_path,
    root_dir_from_path,
    project_main_dir_from_path,
    rolltype_dir_from_path,
    rolltype_from_path,
    foldername_from_path,
    project_name_from_path,
    is_valid_db_path,
)


class Disk(models.Model):
    class Meta:
        db_table = "disk"
        ordering = ["name"]

    disk_serial_number = models.CharField(max_length=120, primary_key=True)

    name = models.CharField(max_length=120, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    size_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    size_remaining_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    size_used_bytes = models.PositiveBigIntegerField(null=True, blank=True)

    last_checked = models.DateTimeField(null=True, blank=True)
    healthstatus = models.CharField(max_length=120, null=True, blank=True)

    total_items_count = models.IntegerField(null=True, blank=True)
    total_duration_sec = models.IntegerField(null=True, blank=True)

    newest_file = models.DateTimeField(null=True, blank=True)
    oldest_file = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.disk_serial_number


class RootDirectory(models.Model):
    class Meta:
        db_table = "root_directory"

    path = models.CharField(max_length=255, unique=True)
    disk = models.ForeignKey(to=Disk, null=True, blank=True, on_delete=models.CASCADE)

    @classmethod
    def path_as_instance(cls, path: str) -> object:
        if not path:
            return None
        obj = cls.objects.filter(path=path).first()
        if not obj:
            obj = cls.objects.create(path=path)
        if obj.disk is None:
            disk_serial_number = disk_from_path(obj.path)
            if disk_serial_number:
                disk_obj = Disk.objects.filter(
                    disk_serial_number=disk_serial_number
                ).first()
                if not disk_obj:
                    disk_obj = Disk.objects.create(
                        disk_serial_number=disk_serial_number
                    )
                obj.disk = disk_obj
                obj.save()
        return obj

    def __str__(self):
        return self.path


class ProjectMainDirectory(models.Model):
    class Meta:
        db_table = "project_main_directory"

    path = models.CharField(max_length=255, unique=True)
    project = models.ForeignKey(
        to="Project", null=True, blank=True, on_delete=models.CASCADE
    )
    root_directory = models.ForeignKey(
        to="RootDirectory", null=True, blank=True, on_delete=models.CASCADE
    )

    @classmethod
    def path_as_instance(cls, path: str) -> object:
        if not path:
            return None
        obj = cls.objects.filter(path=path).first()
        if not obj:
            obj = cls.objects.create(path=path)
        if obj.project is None:
            project_name = project_name_from_path(obj.path)
            if project_name:
                obj.project = Project.objects.get_or_create(name=project_name)[0]
                obj.save()
        if obj.root_directory is None:
            root_dir_path = root_dir_from_path(obj.path)
            if is_valid_db_path(root_dir_path):
                obj.root_dir_path = RootDirectory.path_as_instance(root_dir_path)
                obj.save()
        return obj

    def __str__(self):
        return self.path


class ProjectRollDirectory(models.Model):
    class Meta:
        db_table = "project_roll_directory"

    path = models.CharField(max_length=255, unique=True)
    rolltype = models.CharField(max_length=32, null=True, blank=True)

    project_main_directory = models.ForeignKey(
        to=ProjectMainDirectory, on_delete=models.CASCADE, null=True, blank=True
    )

    # rydd opp
    @classmethod
    def path_as_instance(cls, path: str) -> object:
        if not path:
            return None
        obj = cls.objects.filter(path=path).first()
        if not obj:
            obj = cls.objects.create(path=path)
        if obj.rolltype is None:
            obj.rolltype = rolltype_from_path(obj.path)
        if obj.project_main_directory is None:
            main_dir_path = project_main_dir_from_path(obj.path)
            if is_valid_db_path(main_dir_path):
                obj.project_main_directory = ProjectMainDirectory.path_as_instance(
                    main_dir_path
                )
                obj.save()
        return obj

    def __str__(self):
        return self.path


class LocalDirectory(models.Model):
    class Meta:
        db_table = "local_directory"

    path = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=120, null=True, blank=True)

    parent_foreign = models.ForeignKey(
        to="self", null=True, blank=True, on_delete=models.CASCADE
    )
    parent = models.CharField(max_length=120, null=True, blank=True)

    project_roll_directory = models.ForeignKey(
        to=ProjectRollDirectory, on_delete=models.CASCADE, null=True, blank=True
    )

    @classmethod
    def path_as_instance(cls, path: str) -> object:
        if not path:
            return None
        obj = cls.objects.filter(path=path).first()
        if not obj:
            obj = cls.objects.create(path=path)
        if obj.name is None:
            obj.name = foldername_from_path(obj.path)
            obj.save()
        if obj.project_roll_directory is None:
            roll_dir_path = rolltype_dir_from_path(obj.path)
            if is_valid_db_path(roll_dir_path):
                obj.project_roll_directory = ProjectRollDirectory.path_as_instance(
                    obj.path
                )

        return obj

    def __str__(self):
        return self.path


class LocalFile(models.Model):
    class Meta:
        db_table = "local_file"

    file_path = models.CharField(max_length=255, primary_key=True)
    file_rolltype = models.CharField(
        max_length=255, null=True, blank=True
    )  # denne burde være i directory
    directory_old = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=120, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True, unique=True)
    videoitem = models.ForeignKey(
        to="Videoitem",
        on_delete=models.CASCADE,
        related_name="local_paths",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    directory = models.ForeignKey(
        to=LocalDirectory, on_delete=models.SET_NULL, null=True, blank=True
    )

    def get_directory(self) -> dict:
        directory = self.directory
        return {
            "id": directory.id,
            "path": directory.path,
            "name": directory.name,
            "rolltype": directory.project_roll_directory.rolltype,
            "videoitems": directory.localfile_set.all()
            .annotate(
                id=F("videoitem_id__videoitem_id"),
                lat=F("videoitem_id__gmaps_gps_point_id__lat"),
                lng=F("videoitem_id__gmaps_gps_point_id__lng"),
                thumbnail_count=F("videoitem_id__static_thumbnail_count"),
            )
            .values("id", "lat", "lng", "thumbnail_count"),
        }

    def get_project(self) -> dict:
        project = self.directory.project_roll_directory.project_main_directory.project

        return {"id": project.project_id, "name": project.name}

    def get_disk(self) -> dict:
        disk = (
            self.directory.project_roll_directory.project_main_directory.root_directory.disk
        )

        return {"id": disk.disk_serial_number, "name": disk.name}

    def __str__(self):
        return self.path
