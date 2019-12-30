from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import RiskProfileSerializer


class RiskProfileView(APIView):
    def post(self, request):
        serializer = RiskProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()
