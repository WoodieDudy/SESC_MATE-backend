from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, CustomAnnouncement
from .serializers import UserSerializer
from .services.cache import get_parsed_schedule, get_parsed_announcements
from .services.startup.header_handler import HeaderHandler
from .services.startup.response_json import ResponseJson
from .services.startup.user_handler import UserHandler


class ScheduleView(APIView):
    """Получение расписания"""

    def get(self, request: Request) -> Response:
        """Возвращаем расписание. В запросе параметрами должны быть переданы Класс и День недели"""
        if 'day' in request.query_params and 'group' in request.query_params:
            force_update = 'force_update' in request.query_params and request.query_params[
                'force_update'] == '1'
            schedule = get_parsed_schedule(
                int(request.query_params['day']),
                int(request.query_params['group']),
                force_update
            )

            try:
                return Response(schedule, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    def post(self, request: Request) -> Response:
        response_json = ResponseJson()

        """Working with headers"""
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        """Working with user"""
        user_id: int = request.data['id']
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        if not is_user_in_db:
            serializer = UserSerializer()
            validated_data = {
                'vk_user_id': user_id,
                'group': request.data['group'],
                'first_name': request.data['first_name'],
                'last_name': request.data['last_name'],
                'sex': request.data['sex'],
                'profile_picture_url':
                    request.data['photo_100'] or request.data['photo_200'] or request.data[
                        'photo_max_orig']
            }
            try:
                serializer.create(validated_data=validated_data)
                return Response(validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'success': False,
                    'message': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'success': False,
                'message': 'User already in db'
            }, status=status.HTTP_409_CONFLICT)

    def put(self, request: Request) -> Response:
        response_json = ResponseJson()

        """Working with headers"""
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        """Working with user"""
        user_id: int = int(header_handler.vk_header['vk_user_id'])
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        if is_user_in_db:
            user_object_from_db = User.objects.get(
                vk_user_id=user_id)  # User object for serializing
            # TODO: add first and last name editing through put request
            validated_data = {
                'vk_user_id': user_id,
                'group': request.data['group']
            }

            serializer = UserSerializer(user_object_from_db, data=validated_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(validated_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Bad request'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_401_UNAUTHORIZED)


class StartupInfo(APIView):
    """Get startup info"""

    def get(self, request: Request) -> Response:
        response_json = ResponseJson()

        # Working with headers
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        # Working with user
        user_id: int = int(header_handler.vk_header['vk_user_id'])
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        day: int = request.query_params['day']

        if not is_user_in_db:
            return Response(response_json.setup_didnt_completed, status=status.HTTP_200_OK)

        announcements = get_parsed_announcements()
        custom_announcements = CustomAnnouncement.objects.order_by('-is_pinned')
        serialized_announcements = list(map(
            lambda announcement: {
                'header': announcement.header,
                'content': announcement.content,
                'trustedOrigin': True
            },
            custom_announcements
        ))

        force_update = 'force_update' in request.query_params and request.query_params[
            'force_update'] == '1'
        schedule = get_parsed_schedule(day, user.get_group(), force_update)
        try:
            return Response(response_json.get_normal_response(user, schedule,
                                                              serialized_announcements + announcements),
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
