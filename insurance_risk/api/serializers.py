from rest_framework import serializers

from api.enum import HouseOwnership, Score, UserMaritalStatus


class HouseSerializer(serializers.Serializer):
    ownership_status = serializers.ChoiceField(
        choices=HouseOwnership.choices()
    )


class VehicleSerializer(serializers.Serializer):
    year = serializers.IntegerField()


class UserInputSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    dependents = serializers.IntegerField()
    income = serializers.IntegerField()
    marital_status = serializers.ChoiceField(
        choices=UserMaritalStatus.choices()
    )
    risk_questions = serializers.ListField(child=serializers.IntegerField())
    house = HouseSerializer(required=False)
    vehicle = VehicleSerializer(required=False)


class RiskProfileSerializer(serializers.Serializer):
    auto = serializers.ChoiceField(choices=Score.choices())
    disability = serializers.ChoiceField(choices=Score.choices())
    home = serializers.ChoiceField(choices=Score.choices())
    life = serializers.ChoiceField(choices=Score.choices())
