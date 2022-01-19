from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_jwt_extended import jwt_required
from django_jwt_extended import create_access_token
from django_jwt_extended import create_refresh_token
from django_jwt_extended import get_jwt_identity
from django_jwt_extended import get_jwt


# 로그인 및 토큰 발급하기
def login(request):
    return JsonResponse({
        "access_token": create_access_token("iml"),
        'refresh_token': create_refresh_token('iml'),
    })

# 토큰 리프레시
@jwt_required(refresh=True)
def refresh(request):
    identity = get_jwt_identity(request)
    return JsonResponse({
        "access_token": create_access_token(identity),
        'refresh_token': create_refresh_token(identity),
    })


# 로그인 인증 테스트
@jwt_required()
def user(request):
    identity = get_jwt_identity(request)
    payload = get_jwt(request)
    return JsonResponse({
        'id': identity,
        'raw_jwt': payload,
    })


# 옵셔널 로그인 인증 테스트
@jwt_required(optional=True)
def user_optional(request):
    identity = get_jwt_identity(request)
    payload = get_jwt(request)
    return JsonResponse({
        'id': identity,
        'raw_jwt': payload,
    })


# Rest framework 테스트
class RestAPIView(APIView):

    @jwt_required()
    def get(self, request):
        identity = get_jwt_identity(request)
        payload = get_jwt(request)
        return Response({
            'id': identity,
            'raw_jwt': payload,
        })

    @jwt_required()
    def post(self, request):
        identity = get_jwt_identity(request)
        payload = get_jwt(request)
        return Response({
            'id': identity,
            'raw_jwt': payload,
        })

    @jwt_required()
    def put(self, request):
        identity = get_jwt_identity(request)
        payload = get_jwt(request)
        return Response({
            'id': identity,
            'raw_jwt': payload,
        })

    @jwt_required()
    def delete(self, request):
        identity = get_jwt_identity(request)
        payload = get_jwt(request)
        return Response({
            'id': identity,
            'raw_jwt': payload,
        })


# Rest framework Func 테스트
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def rest_user(request, hello: str):
    identity = get_jwt_identity(request)
    payload = get_jwt(request)
    return Response({
        'id': identity,
        'raw_jwt': payload,
        'hello': hello,
    })