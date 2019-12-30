from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import UserInputSerializer, RiskProfileSerializer


class RiskProfileView(APIView):
    def post(self, request):
        serializer = UserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        scores = RiskProfileSerializer(data={
            "auto": "regular",
            "disability": "ineligible",
            "home": "economic",
            "life": "regular"
        })
        scores.is_valid(raise_exception=True)
        return Response(data=scores.data)
