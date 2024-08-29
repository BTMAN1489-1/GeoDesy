from rest_framework import serializers
from utils.geo import Coord, Geometry
from main_app.models import GeoPoint


class GeoPointSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    radius = serializers.FloatField(min_value=10, max_value=40000)

    def _create_response(self, validated_data):
        latitude = validated_data["latitude"]
        longitude = validated_data["longitude"]
        radius = validated_data["radius"]

        coord = Coord(latitude=latitude, longitude=longitude)
        precision = Geometry.get_precision_by_length(length=radius)
        points = GeoPoint.objects.nearby_points(coord.degrees.latitude, coord.degrees.longitude, precision)

        response = []
        for point in points:
            response.append(
                {
                    "latitude": point.latitude,
                    "longitude": point.longitude,
                    "guid": point.guid
                }
            )

        return response

    def get_response(self):
        response = self._create_response(self.validated_data)
        return response
