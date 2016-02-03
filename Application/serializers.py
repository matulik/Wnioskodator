#coding=UTF-8

from Application.models import *

from rest_framework import serializers

from django.utils import timezone

class ApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    dateAdded = serializers.DateTimeField(read_only=True)
    dateLastEdited = serializers.DateTimeField(read_only=True)
    applicationNumber = serializers.CharField(max_length=50, required=True)
    applicationOwner = serializers.CharField(max_length=50, required=True)
    applicationTitle = serializers.CharField(max_length=50, required=True)
    firstViewBy = serializers.CharField(max_length=50, required=True)
    secondViewBy = serializers.CharField(max_length=50, required=True)
    firstStageOpinion = serializers.CharField(max_length=50, required=True)
    additionalDescription = serializers.CharField(max_length=150, required=True)

    def create(self, validated_data):
        return Application.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.dateLastEdited = timezone.now()
        instance.applicationNumber = validated_data.get('applicationNumber', instance.applicationNumber)
        instance.applicationOwner = validated_data.get('applicationOwner', instance.applicationOwner)
        instance.applicationTitle = validated_data.get('applicationTitle', instance.applicationTitle)
        instance.firstViewBy = validated_data.get('firstViewBy', instance.firstViewBy)
        instance.secondViewBy = validated_data.get('secondViewBy', instance.secondViewBy)
        instance.firstStageOpinion = validated_data.get('firstStageOpinion', instance.firstStageOpinion)
        instance.additionalDescription = validated_data.get('additionalDescription', instance.additionalDescription)
        instance.save()
        return instance
