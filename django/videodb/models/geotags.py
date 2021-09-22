from django.db import models
from django.forms.models import model_to_dict
from time import sleep
from timeit import default_timer as timer
import geopy.distance
from ..utils.functions.geographical import get_bounding_box
from ..utils.functions.geocoding import get_reverse_geotags_gmaps


class ScheduledReverseGeotag(models.Model):
    class Meta:
        db_table = 'scheduled_reverse_geotag'

    gps_point = models.ForeignKey(to='GmapsGpsPoint', on_delete=models.CASCADE, null=True, blank=True)
    geotag_level_1 = models.ForeignKey(to='GeotagLevel1', on_delete=models.CASCADE, null=True, blank=True)

    lat = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    @classmethod
    def gps_point_is_scheduled(cls, gps_point):
        return bool(cls.objects.filter(gps_point=gps_point).exists())

    @classmethod
    def schedule_if_not_scheduled(cls, gps_point):
        if not cls.gps_point_is_scheduled(gps_point):
            cls.objects.create(gps_point=gps_point, lat=gps_point.lat, lng=gps_point.lng)

    @classmethod
    def get_gmaps_geocode_dict(cls,latlng):
        return get_reverse_geotags_gmaps(latlng)

    @classmethod
    def clear_completed_geotags(cls):
        cls.objects.filter(
            geotag_level_1_id__isnull = False
        ).delete()
        return

    @classmethod
    def batch_reverse_geocode(cls):
        def throttle(time_start, time_end, condition=True):
            max_throttle = 0.05
            if not condition or (max_throttle - time_end - time_start) < 0:
                return
            return sleep((max_throttle - time_end-time_start))

        new_geotags = []

        qs = cls.objects.all()
        qs_len = len(qs)

        for scheduled in qs:
            geotag = None
            for new_geotag in new_geotags:
                if all([
                    new_geotag.lat_min < scheduled.lat,
                    new_geotag.lat_max > scheduled.lat,
                    new_geotag.lng_min < scheduled.lng,
                    new_geotag.lng_max > scheduled.lng
                ]):
                    geotag = new_geotag
                    break

            if not geotag:
                time_start = timer()
                dict_ = cls.get_gmaps_geocode_dict((scheduled.lat, scheduled.lng,))
                if not dict_:
                    continue
                geotag = GeotagLevel1.new_from_dict(dict_)
                if geotag:
                    new_geotags.append(geotag)
                else:
                    continue

            scheduled.geotag_level_1 = geotag
            scheduled.save()

            gps_point = scheduled.gps_point
            gps_point.geotag_level_1 = geotag
            gps_point.save()

            time_end = timer()
            throttle(time_start, time_end, condition=(qs_len >= 50))

        cls.clear_completed_geotags()

class GeotagLevel5(models.Model):
    class Meta: db_table = 'geotag_level_5'
    
    lat_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lat_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    displayname_short = models.CharField(max_length=255, null=True, blank=True)
    displayname_full = models.CharField(max_length=255, null=True, blank=True)

    postal_town = models.CharField(max_length=120, null=True, blank=True)
    locality = models.CharField(max_length=120, null=True, blank=True)
    county = models.CharField(max_length=120, null=True, blank=True)
    municipality = models.CharField(max_length=120, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(to='UniqueLocationDisplayname', on_delete=models.SET_NULL, null=True, blank=True)

    def get_boundingbox_areal(self):
        return self.distances['ns'] * self.distances['ew']

    @classmethod
    def new_from_dict(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None

        if not "level_5" in dict_ or not isinstance(dict_["level_5"], dict):
            return None

        if not all([
            "lat_min" in dict_["level_5"],
            "lat_max" in dict_["level_5"],
            "lng_min" in dict_["level_5"],
            "lng_max" in dict_["level_5"],
        ]):
            return None

        existing = cls.objects.filter(
            lat_min = dict_['level_5']['lat_min'],
            lat_max = dict_['level_5']['lat_max'],
            lng_min = dict_['level_5']['lng_min'],
            lng_max = dict_['level_5']['lng_max'],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min = dict_['level_5']['lat_min'],
            lat_max = dict_['level_5']['lat_max'],
            lng_min = dict_['level_5']['lng_min'],
            lng_max = dict_['level_5']['lng_max'],

            displayname_short = dict_['level_5']['displayname_short'],
            displayname_full = dict_['level_5']['displayname_full'],

            postal_town = dict_['level_5']['postal_town'],
            locality = dict_['level_5']['locality'],
            county = dict_['level_5']['county'],
            municipality = dict_['level_5']['municipality'],
            country_code = dict_['level_5']['country_code'],
            postal_code = dict_['level_5']['postal_code'],

            distances = dict_['level_5']['distances'],
        )

        return new_object

    @classmethod
    def get_by_bounds(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None

        if not all([
            "lat_min" in dict_,
            "lat_max" in dict_,
            "lng_min" in dict_,
            "lng_max" in dict_,
        ]):
            return None

        qs = cls.objects.filter(
            lat_min__lt=dict_['lat_min'],
            lat_max__gt=dict_['lat_max'],
            lng_min__lt=dict_['lng_min'],
            lng_max__gt=dict_['lng_max'])

        if not qs: 
            return None

        obj = sorted(
            qs,
            key=lambda x: (x.get_boundingbox_areal())
        )[0]

        return obj



class GeotagLevel4(models.Model):
    class Meta: db_table = 'geotag_level_4'
    
    lat_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lat_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    displayname_short = models.CharField(max_length=255, null=True, blank=True)
    displayname_full = models.CharField(max_length=255, null=True, blank=True)

    postal_town = models.CharField(max_length=120, null=True, blank=True)
    locality = models.CharField(max_length=120, null=True, blank=True)
    county = models.CharField(max_length=120, null=True, blank=True)
    municipality = models.CharField(max_length=120, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(to='UniqueLocationDisplayname', on_delete=models.SET_NULL, null=True, blank=True)

    geotag_level_5 = models.ForeignKey(to='GeotagLevel5', null=True, blank=True, on_delete=models.CASCADE)

    def get_boundingbox_areal(self):
        return self.distances['ns'] * self.distances['ew']

    @classmethod
    def new_from_dict(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None
        if not "level_4" in dict_ or not isinstance(dict_["level_4"], dict):
            return None
        if not all([
            "lat_min" in dict_["level_4"],
            "lat_max" in dict_["level_4"],
            "lng_min" in dict_["level_4"],
            "lng_max" in dict_["level_4"],
        ]):
            return None

        existing = cls.objects.filter(
            lat_min = dict_['level_4']['lat_min'],
            lat_max = dict_['level_4']['lat_max'],
            lng_min = dict_['level_4']['lng_min'],
            lng_max = dict_['level_4']['lng_max'],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min = dict_['level_4']['lat_min'],
            lat_max = dict_['level_4']['lat_max'],
            lng_min = dict_['level_4']['lng_min'],
            lng_max = dict_['level_4']['lng_max'],

            displayname_short = dict_['level_4']['displayname_short'],
            displayname_full = dict_['level_4']['displayname_full'],

            postal_town = dict_['level_4']['postal_town'],
            locality = dict_['level_4']['locality'],
            county = dict_['level_4']['county'],
            municipality = dict_['level_4']['municipality'],
            country_code = dict_['level_4']['country_code'],
            postal_code = dict_['level_4']['postal_code'],

            distances = dict_['level_4']['distances'],
        )

        level_5 = GeotagLevel5.get_by_bounds(dict(
            lat_min = dict_['level_4']['lat_min'],
            lat_max = dict_['level_4']['lat_max'],
            lng_min = dict_['level_4']['lng_min'],
            lng_max = dict_['level_4']['lng_max'],))

        if not level_5:
            level_5 = GeotagLevel5.new_from_dict(dict_)

        if level_5:
            new_object.geotag_level_5 = level_5
            new_object.save()

        return new_object

    @classmethod
    def get_by_bounds(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None
        if not all([
            "lat_min" in dict_,
            "lat_max" in dict_,
            "lng_min" in dict_,
            "lng_max" in dict_,
        ]):
            return None

        qs = cls.objects.filter(
            lat_min__lt=dict_['lat_min'],
            lat_max__gt=dict_['lat_max'],
            lng_min__lt=dict_['lng_min'],
            lng_max__gt=dict_['lng_max'])

        if not qs: 
            return None

        obj = sorted(
            qs,
            key=lambda x: (x.get_boundingbox_areal())
        )[0]

        return obj



class GeotagLevel3(models.Model):
    class Meta: db_table = 'geotag_level_3'
    
    lat_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lat_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    displayname_short = models.CharField(max_length=255, null=True, blank=True)
    displayname_full = models.CharField(max_length=255, null=True, blank=True)

    postal_town = models.CharField(max_length=120, null=True, blank=True)
    locality = models.CharField(max_length=120, null=True, blank=True)
    county = models.CharField(max_length=120, null=True, blank=True)
    municipality = models.CharField(max_length=120, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(to='UniqueLocationDisplayname', on_delete=models.SET_NULL, null=True, blank=True)

    geotag_level_4 = models.ForeignKey(to='GeotagLevel4', null=True, blank=True, on_delete=models.CASCADE)

    def get_boundingbox_areal(self):
        return self.distances['ns'] * self.distances['ew']

    @classmethod
    def new_from_dict(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None

        if not "level_3" in dict_ or not isinstance(dict_["level_3"], dict):
            return None

        if not all([
            "lat_min" in dict_["level_3"],
            "lat_max" in dict_["level_3"],
            "lng_min" in dict_["level_3"],
            "lng_max" in dict_["level_3"],
        ]):
            return None

        existing = cls.objects.filter(
            lat_min = dict_['level_3']['lat_min'],
            lat_max = dict_['level_3']['lat_max'],
            lng_min = dict_['level_3']['lng_min'],
            lng_max = dict_['level_3']['lng_max'],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min = dict_['level_3']['lat_min'],
            lat_max = dict_['level_3']['lat_max'],
            lng_min = dict_['level_3']['lng_min'],
            lng_max = dict_['level_3']['lng_max'],

            displayname_short = dict_['level_3']['displayname_short'],
            displayname_full = dict_['level_3']['displayname_full'],

            postal_town = dict_['level_3']['postal_town'],
            locality = dict_['level_3']['locality'],
            county = dict_['level_3']['county'],
            municipality = dict_['level_3']['municipality'],
            country_code = dict_['level_3']['country_code'],
            postal_code = dict_['level_3']['postal_code'],

            distances = dict_['level_3']['distances'],
        )
        level_4 = GeotagLevel4.get_by_bounds(dict(
            lat_min = dict_['level_3']['lat_min'],
            lat_max = dict_['level_3']['lat_max'],
            lng_min = dict_['level_3']['lng_min'],
            lng_max = dict_['level_3']['lng_max'],))

        if not level_4:
            level_4 = GeotagLevel4.new_from_dict(dict_)

        if level_4:
            new_object.geotag_level_4 = level_4
            new_object.save()

        return new_object

    @classmethod
    def get_by_bounds(cls,dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None
        if not all([
            "lat_min" in dict_,
            "lat_max" in dict_,
            "lng_min" in dict_,
            "lng_max" in dict_,
        ]):
            return None

        qs = cls.objects.filter(
            lat_min__lt=dict_['lat_min'],
            lat_max__gt=dict_['lat_max'],
            lng_min__lt=dict_['lng_min'],
            lng_max__gt=dict_['lng_max'])

        if not qs: 
            return None

        obj = sorted(
            qs,
            key=lambda x: (x.get_boundingbox_areal())
        )[0]

        return obj



class GeotagLevel2(models.Model):
    class Meta: db_table = 'geotag_level_2'
    
    lat_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lat_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    displayname_short = models.CharField(max_length=255, null=True, blank=True)
    displayname_full = models.CharField(max_length=255, null=True, blank=True)

    postal_town = models.CharField(max_length=120, null=True, blank=True)
    locality = models.CharField(max_length=120, null=True, blank=True)
    county = models.CharField(max_length=120, null=True, blank=True)
    municipality = models.CharField(max_length=120, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(to='UniqueLocationDisplayname', on_delete=models.SET_NULL, null=True, blank=True)

    geotag_level_3 = models.ForeignKey(to='GeotagLevel3', null=True, blank=True, on_delete=models.CASCADE)

    def get_boundingbox_areal(self):
        return self.distances['ns'] * self.distances['ew']

    @classmethod
    def new_from_dict(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None
        if not "level_2" in dict_ or not isinstance(dict_["level_2"], dict):
            return None
        if not all([
            "lat_min" in dict_["level_2"],
            "lat_max" in dict_["level_2"],
            "lng_min" in dict_["level_2"],
            "lng_max" in dict_["level_2"],
        ]):
            return None

        existing = cls.objects.filter(
            lat_min = dict_['level_2']['lat_min'],
            lat_max = dict_['level_2']['lat_max'],
            lng_min = dict_['level_2']['lng_min'],
            lng_max = dict_['level_2']['lng_max'],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min = dict_['level_2']['lat_min'],
            lat_max = dict_['level_2']['lat_max'],
            lng_min = dict_['level_2']['lng_min'],
            lng_max = dict_['level_2']['lng_max'],

            displayname_short = dict_['level_2']['displayname_short'],
            displayname_full = dict_['level_2']['displayname_full'],

            postal_town = dict_['level_2']['postal_town'],
            locality = dict_['level_2']['locality'],
            county = dict_['level_2']['county'],
            municipality = dict_['level_2']['municipality'],
            country_code = dict_['level_2']['country_code'],
            postal_code = dict_['level_2']['postal_code'],

            distances = dict_['level_2']['distances'],
        )

        level_3 = GeotagLevel3.get_by_bounds(dict(
            lat_min = dict_['level_2']['lat_min'],
            lat_max = dict_['level_2']['lat_max'],
            lng_min = dict_['level_2']['lng_min'],
            lng_max = dict_['level_2']['lng_max'],))

        if not level_3:
            level_3 = GeotagLevel3.new_from_dict(dict_)

        if level_3:
            new_object.geotag_level_3 = level_3
            new_object.save()

        return new_object

    @classmethod
    def get_by_bounds(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None
        if not all([
            "lat_min" in dict_,
            "lat_max" in dict_,
            "lng_min" in dict_,
            "lng_max" in dict_,
        ]):
            return None

        qs = cls.objects.filter(
            lat_min__lt=dict_['lat_min'],
            lat_max__gt=dict_['lat_max'],
            lng_min__lt=dict_['lng_min'],
            lng_max__gt=dict_['lng_max'])

        if not qs: 
            return None

        obj = sorted(
            qs,
            key=lambda x: (x.get_boundingbox_areal())
        )[0]

        return obj


class GeotagLevel1(models.Model):
    class Meta: db_table = 'geotag_level_1_correct'
    
    lat_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lat_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_min = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng_max = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    displayname_short = models.CharField(max_length=255, null=True, blank=True)
    displayname_full = models.CharField(max_length=255, null=True, blank=True)

    postal_town = models.CharField(max_length=120, null=True, blank=True)
    locality = models.CharField(max_length=120, null=True, blank=True)
    county = models.CharField(max_length=120, null=True, blank=True)
    municipality = models.CharField(max_length=120, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(to='UniqueLocationDisplayname', on_delete=models.SET_NULL, null=True, blank=True)

    geotag_level_2 = models.ForeignKey(to='GeotagLevel2', null=True, blank=True, on_delete=models.CASCADE)

    def get_boundingbox_areal(self):
        return self.distances['ns'] * self.distances['ew']

    def get_videoitems(self,limit):
        return [x.get_videoitems(limit) for x in self.gps_points.all()[:limit]]

    def get_displayname_short(self):
        list_ = self.displayname_short.split(",")
        dict_ = model_to_dict(self, fields=list_)

        displayname_short = ", ".join(
            dict_[x] for x in list_
                if all([
                    x is not None,
                    dict_[x]
                ])
            ).replace("fylke","")

        return displayname_short.strip()

    @classmethod
    def new_from_dict(cls, dict_):
        if not dict_ or not isinstance(dict_, dict):
            return None
        if not "level_1" in dict_ or not isinstance(dict_["level_1"], dict):
            return None
        if not all([
            "lat_min" in dict_["level_1"],
            "lat_max" in dict_["level_1"],
            "lng_min" in dict_["level_1"],
            "lng_max" in dict_["level_1"],
        ]):
            return None

        existing = cls.objects.filter(
            lat_min = dict_['level_1']['lat_min'],
            lat_max = dict_['level_1']['lat_max'],
            lng_min = dict_['level_1']['lng_min'],
            lng_max = dict_['level_1']['lng_max'],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min = dict_['level_1']['lat_min'],
            lat_max = dict_['level_1']['lat_max'],
            lng_min = dict_['level_1']['lng_min'],
            lng_max = dict_['level_1']['lng_max'],

            displayname_short = dict_['level_1']['displayname_short'],
            displayname_full = dict_['level_1']['displayname_full'],

            postal_town = dict_['level_1']['postal_town'],
            locality = dict_['level_1']['locality'],
            county = dict_['level_1']['county'],
            municipality = dict_['level_1']['municipality'],
            country_code = dict_['level_1']['country_code'],
            postal_code = dict_['level_1']['postal_code'],

            distances = dict_['level_1']['distances'],
        )

        level_2 = GeotagLevel2.get_by_bounds(dict(
            lat_min = dict_['level_1']['lat_min'],
            lat_max = dict_['level_1']['lat_max'],
            lng_min = dict_['level_1']['lng_min'],
            lng_max = dict_['level_1']['lng_max'],))

        if not level_2:
            level_2 = GeotagLevel2.new_from_dict(dict_)

        if level_2:
            new_object.geotag_level_2 = level_2
            new_object.save()

        return new_object

    @classmethod
    def get_by_latlng(cls,latlng):
        (lat,lng) = latlng
        
        qs = cls.objects.filter(
            lat_min__lt=lat,
            lat_max__gt=lat,
            lng_min__lt=lng,
            lng_max__gt=lng)

        if not qs: 
            return None

        obj = sorted(
            qs,
            key=lambda x: (x.get_boundingbox_areal())
        )[0]

        return obj


class GmapsGpsPoint(models.Model):
    class Meta: db_table = 'gmaps_gpspoint'

    lat = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)  
    lng = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    geotag_level_1 = models.ForeignKey(to='GeotagLevel1', null=True, blank=True, on_delete=models.CASCADE, related_name='gps_points')

    custom_displayname = models.CharField(max_length=120, null=True, blank=True)

    def get_videoitems(self,limit):
        return self.videoitems.all()[:limit]

    def get_displayname_short(self):
        if self.custom_displayname:
            return self.custom_displayname
        if self.geotag_level_1:
            return self.geotag_level_1.get_displayname_short()

    @classmethod
    def get_by_latlng(cls, latlng):
        (lat, lng) = latlng
        bounds_2m = get_bounding_box(lat,lng,0.0002)

        qs = GmapsGpsPoint.objects.filter(
            lat__gt=bounds_2m['lat_min'],
            lat__lt=bounds_2m['lat_max'],
            lng__gt=bounds_2m['lng_min'],
            lng__lt=bounds_2m['lng_max'],
        )

        obj = None
        if qs:
            for gps_point in qs:
                # snap to existing point within 1 meter
                if geopy.distance.distance(latlng, (gps_point.lat, gps_point.lng,)).meters <= 1:
                    obj = gps_point
                    break

        if obj is None:
            obj = GmapsGpsPoint.objects.create(lat = lat, lng = lng)

        if obj.geotag_level_1 is None:
            geotag = GeotagLevel1.get_by_latlng(latlng)
            if not geotag:
                ScheduledReverseGeotag.schedule_if_not_scheduled(obj)
            else:
                obj.geotag_level_1 = geotag
                obj.save()

        return obj