from apps.interactions.models import Comment, CommentLike, Dislike, Follower, Like
from rest_framework import serializers

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Like
        
        
class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Dislike

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  
    class Meta:
        fields = '__all__'
        model = Comment
        
        
class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CommentLike
        



