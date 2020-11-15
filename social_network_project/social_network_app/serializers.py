from rest_framework import serializers

from .models import SimplePost, Like, CustomUser


class SimplePostSerializer(serializers.ModelSerializer):
	class Meta:
		model = SimplePost
		fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Like
		fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['last_login', 'last_request']
