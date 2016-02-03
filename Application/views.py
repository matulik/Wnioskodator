#coding=UTF-8

from django.shortcuts import redirect, render_to_response, RequestContext
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from User.models import Login
from Application.models import Application
from Application.serializers import ApplicationSerializer

### API VIEWS ###
@csrf_exempt
@api_view(['GET','POST'])
def applications_list(request):
    if not Login.auth(request):
        msg = u'Musisz być zalogowany by korzystać z usługi. Zaloguj się i spróbuj ponownie'
        return render_to_response('User/login.html', { 'msg': msg }, context_instance=RequestContext(request))
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
@csrf_exempt
def application_detail(request, pk):
    if not Login.auth(request):
        msg = u'Musisz być zalogowany by korzystać z usługi. Zaloguj się i spróbuj ponownie'
        return render_to_response('User/login.html', { 'msg': msg }, context_instance=RequestContext(request))
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


