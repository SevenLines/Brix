from rest_framework import serializers

from apps.schedule.models import RaspisZaoch


class BrixSetNagruzkaSerializers(serializers.Serializer):
    raspnagr_id = serializers.IntegerField()
    aud = serializers.IntegerField(required=False)
    date = serializers.DateField()
    pair = serializers.IntegerField()

    def save(self, **kwargs):
        rz, _ = RaspisZaoch.objects.get_or_create(
            raspnagr_id=self.validated_data['raspnagr_id'],
            dt=self.validated_data['date'],
            para=self.validated_data['pair'],
            defaults={
                "hours": 2
            }
        )

        if 'aud' in self.validated_data:
            rz.aud = self.validated_data.get('aud', None)

        rz.hours = 2
        rz.save()

        return rz


class BrixGetRaspisSerializer(serializers.Serializer):
    kontid = serializers.IntegerField()


class BrixModuleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    kont_id = serializers.IntegerField()
    title = serializers.CharField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()