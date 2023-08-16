from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatForm, Review


class ReviewSerializer(serializers.ModelSerializer):
    # rating = serializers.FloatField()
    review_user_name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Review
        exclude = ('watchlist','review_user',)

    def get_review_user_name(self, obj):
        return obj.review_user.username if obj.review_user else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['review_user'] = representation.pop('review_user_name')
        return representation


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)  # Updated field name

    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatFormSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)  # Updated field name

    class Meta:
        model = StreamPlatForm
        fields = "__all__"
