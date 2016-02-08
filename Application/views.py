#coding=UTF-8

from django.shortcuts import redirect, render_to_response, RequestContext

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from User.models import User, Login
from Application.models import Application
from Application.serializers import ApplicationSerializer


### AUTH ###
@api_view(['POST'])
def getAuthToken(request):
    if Login.login(request) and request.method == 'POST':
        data = {}
        user = User.objects.get(id=request.session['id'])
        data['TOKEN'] = user.token
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)


### API VIEWS ###
@api_view(['GET','POST'])
def applications_list(request):
    if not Login.tokenAuth(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        if request.method == 'GET':
            aps = Application.objects.all()
            serializer = ApplicationSerializer(aps, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'POST':
            serializer = ApplicationSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # IF all another is fail
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def application_detail(request, pk):
    if not Login.tokenAuth(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        # If exists
        try:
            ap = Application.objects.get(id=pk)
        except Application.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ApplicationSerializer(ap, context={'request', request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = ApplicationSerializer(ap, context={'request':request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            ap.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # If another is fail
        return Response(status=status.HTTP_400_BAD_REQUEST)


