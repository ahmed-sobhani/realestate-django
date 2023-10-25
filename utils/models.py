import json
import six

from django.db import models
from django.contrib.gis.geos import Point
from rest_framework import serializers


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def soft_delete(self, force_save=True):
        self.deleted = True
        if force_save:
            self.save()

    def un_soft_delete(self, force_save=True):
        self.deleted = False
        if force_save:
            self.save()


class PointSerializer(serializers.Field):
    """
    Expected input format:
        {
        "latitude": 49.8782482189424,
         "longitude": 24.452545489
        }
    """
    type_name = 'PointField'
    type_label = 'point'

    default_error_messages = {
        'invalid': 'Enter a valid location.',
    }

    def to_internal_value(self, value):
        """
        Parse json data and return a point object
        """
        if value in (None, '', [], (), {}) and not self.required:
            return None

        if isinstance(value, six.string_types):
            try:
                value = value.replace("'", '"')
                value = json.loads(value)
            except ValueError:
                self.fail('invalid')

        if value and isinstance(value, dict):
            try:
                return Point(
                    float(value['longitude']),
                    float(value['latitude'])
                )
            except (TypeError, ValueError, KeyError):
                self.fail('invalid')
        self.fail('invalid')

    def to_representation(self, value):
        if isinstance(value, Point):
            value = {
                "latitude": value.y,
                "longitude": value.x
            }
        return value
