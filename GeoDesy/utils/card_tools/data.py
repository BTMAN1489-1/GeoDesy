__all__ = (
    "displayed_Card_fields", "displayed_GeoPoint_fields", "displayed_Photo_fields", "owners", "sorted_fields",
    "mapper_related_GeoPoint_fields", "mapper_related_Federal_fields", "mapper_related_fields",
    "reverse_mapper_related_fields", "displayed_fields", "CardData"
)


displayed_Card_fields = {"status", "execute_date", "identification_pillar",
                         "monolith_one", "monolith_two", "monolith_three_and_four", "sign_height_above_ground_level",
                         "outdoor_sign", "ORP_one", "ORP_two", "trench", "satellite_surveillance", "type_of_sign",
                         "point_index", "name_point", "year_of_laying", "type_of_center", "height_above_sea_level",
                         "trapezoids", "datetime_creation", "datetime_inspection"}

displayed_GeoPoint_fields = {"latitude", "longitude", "federal_subject", "federal_district"}
displayed_Photo_fields = {"photos"}
owners = {"executor", "inspector"}

sorted_fields = {"datetime_creation", "datetime_inspection"}

mapper_related_GeoPoint_fields = {"latitude": "coordinates__latitude", "longitude": "coordinates__longitude"}

mapper_related_Federal_fields = {"federal_subject": "coordinates__subject__name",
                                 "federal_district": "coordinates__subject__district__name"
                                 }

mapper_related_fields = mapper_related_Federal_fields | mapper_related_GeoPoint_fields

reverse_mapper_related_fields = {"latitude": "coordinates__latitude", "longitude": "coordinates__longitude",
                                 "federal_subject": "coordinates__subject__name",
                                 "federal_district": "coordinates__subject__district__name"
                                 }

displayed_fields = displayed_Card_fields | displayed_GeoPoint_fields | owners | displayed_Photo_fields


class CardData:
    def __init__(self, obj_model):
        self.card = obj_model
        self.coordinates = obj_model.coordinates
        self.executor = obj_model.executor
        self.inspector = obj_model.inspector
        self.photos = obj_model.photos.all()
