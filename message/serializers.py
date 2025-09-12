from rest_framework import serializers
from main_app.models import CustomUser
from .models import Message, Project, Channel, Comment, MessageLike

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_type', 'profile_pic', 'address']  
        # ✅ Add more fields if needed

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  

    class Meta:
        model = Message
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class MessageLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MessageLike
        fields = '__all__'
