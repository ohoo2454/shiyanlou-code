from rest_framework import serializers
from app01 import models


class PublisherSerializer(serializers.Serializer):
    name = serializers.CharField()


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    pub_info = serializers.SerializerMethodField(read_only=True)
    authors_info = serializers.SerializerMethodField(read_only=True)

    def get_pub_info(self, obj):
        return PublisherSerializer(obj.pub).data

    def get_authors_info(self, obj):
        return AuthorSerializer(obj.authors.all(), many=True).data

    class Meta:
        model = models.Book
        fields = "__all__"
        # depth = 1
        extra_kwargs = {
            'pub': {'write_only': True},
            'authors': {'write_only': True},
        }
