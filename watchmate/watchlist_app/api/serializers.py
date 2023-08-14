from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatForm, Review


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()

    class Meta:
        model = Review
        fields = "__all__"


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
