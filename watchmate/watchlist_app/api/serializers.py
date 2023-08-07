from rest_framework import serializers
from watchlist_app.models import WatchList


class StreamPlatFormSerailizer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatForm
        fields = "__all__"


    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.validationError("the title and the story lines must be d/f")
            



class WatchListSerializer(serializers.ModelSerializer):

    len_title = serializers.SerializerMethodField()

    class Meta:
        model = WatchList
        fields = "__all__"


    def get_len_title(self, object):
        return len(object.title)
    



# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField(validators = [name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance


#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.validationError("the names should be different")
#         else:
#             return data

#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short!")
#         else:
#             return value