import re
from django.db import models
from .unique_searchfilter import UniqueKeyword

class Keyword(models.Model):
    class Meta:
        db_table = 'keyword'
        unique_together = ['keyword', 'videoitem']
        ordering = ['keyword']

    keyword = models.CharField(max_length=120)
    videoitem = models.ForeignKey(to='Videoitem', blank=True, null=True, on_delete=models.CASCADE)
    unique_keyword = models.ForeignKey(to='UniqueKeyword', blank=True, null=True, on_delete=models.SET_NULL, related_name='keyword_videoitem_link')

    # ta dette ut av model
    @classmethod
    def clean_string(cls, string: str) -> str:
        string = string.lower().strip()
        if string[-1] in [',', '.']:
            return cls.clean_string(string[:-1])
        return string

    # og dette
    @classmethod
    def validate_string(cls, string: str) -> str:
        pattern = "^[4-9][a-cA-C\+-]?[\+-]?$|^[a-zA-ZæøåÆØÅ][a-zA-ZæøåÆØÅ]+$"
        string = cls.clean_string(string)
        if not re.search(pattern, string):
            return None
        if string == cls.clean_string(string):
            return string
        return cls.clean_string(cls.validate_string(string))

    @classmethod
    def create_if_valid(cls, keyword, videoitem=None):
        valid_string = cls.validate_string(keyword)
        if valid_string:
            return cls.objects.get_or_create(
                keyword = valid_string,
                videoitem = videoitem
            )
        return None

    @classmethod
    def validate_and_clean_all(cls): 
        qs = cls.objects.all()
        for obj in qs:
            valid = cls.validate_string(obj.keyword)
            if not valid:
                continue
            if valid != obj.keyword:
                obj.keyword = valid
                obj.save()
            if obj.unique_keyword is None:
                unique_keyword = UniqueKeyword.objects.get_or_create(keyword=obj.keyword)
                obj.unique_keyword = unique_keyword[0] if unique_keyword else None
                obj.save()