from rest_framework import serializers

from .models import KYCFile


class KYCFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    file_type = serializers.CharField()
    file_type_info = serializers.CharField(source='get_file_type_display', read_only=True)

    class Meta:
        model = KYCFile
        fields = (
            'id',
            'file_type',
            'file_type_info',
            'file',
        )

    def create(self, validated_data):
        obj, _ = KYCFile.objects.get_or_create(
                    investor=self.context['request'].user.investor,
                    file_type=validated_data['file_type'],
                )
        obj.file = validated_data['file']
        obj.save()
        return obj
