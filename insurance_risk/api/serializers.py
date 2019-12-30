from rest_framework import serializers


class HouseSerializer(serializers.Serializer):
    ownership_status = serializers.ChoiceField(choices=('owned', 'mortgaged'))


class VehicleSerializer(serializers.Serializer):
    year = serializers.IntegerField()


class RiskProfileSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    dependents = serializers.IntegerField()
    income = serializers.IntegerField()
    marital_status = serializers.ChoiceField(choices=('single', 'married'))
    risk_questions = serializers.ListField(child=serializers.IntegerField())
    house = HouseSerializer(required=False)
    vehicle = VehicleSerializer(required=False)
