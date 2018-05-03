from rest_framework import serializers
from firstApp.models import Visitor,Chair


class VisitorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visitor
        fields = ('fullName','email','visitedStartup', 'cinId')

class ChairSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chair
        fields = ('a','b','c','d','x','y','z','v','w')
