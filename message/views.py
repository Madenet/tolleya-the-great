from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Message, Channel, Project, MessageLike
from .serializers import MessageSerializer, ProjectSerializer, UserSerializer
from main_app.models import CustomUser

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and request.user.is_authenticated:
            response.data['user'] = UserSerializer(request.user).data
        return response

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def messages_view(request):
    if request.method == 'GET':
        channel_id = request.GET.get('channel', 1)
        messages = Message.objects.filter(channel_id=channel_id).order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['sender'] = request.user.id
        data['channel'] = data.get('channel', 1)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save()

            # Push to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{message.channel.id}',
                {
                    'type': 'send_message',
                    'message': MessageSerializer(message).data
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def message_like_view(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=404)

    if request.method == 'POST':
        MessageLike.objects.get_or_create(message=message, user=request.user)
        return Response({'liked': True, 'likes_count': message.likes.count()})

    elif request.method == 'DELETE':
        MessageLike.objects.filter(message=message, user=request.user).delete()
        return Response({'liked': False, 'likes_count': message.likes.count()})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file_view(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)

    file = request.FILES['file']
    content = request.data.get('content', '')
    channel_id = request.data.get('channel', 1)

    if file.content_type.startswith('image/'):
        message_type = 'image'
    elif file.content_type.startswith('video/'):
        message_type = 'video'
    else:
        message_type = 'file'

    from django.core.files.storage import default_storage
    file_path = default_storage.save(f'uploads/{file.name}', file)
    file_url = default_storage.url(file_path)

    message = Message.objects.create(
        channel_id=channel_id,
        sender=request.user,
        content=content,
        message_type=message_type,
        file_url=file_url,
        file_name=file.name,
        file_type=file.content_type,
    )

    return Response(MessageSerializer(message).data)

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
