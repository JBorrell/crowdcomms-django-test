from datetime import datetime, timedelta

from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import UserVisit


class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):
        timeframe = timezone.now() - timedelta(hours=1)
        all_visitors = UserVisit.objects.all()
        recent_visitors = UserVisit.objects.filter(last_seen__gt=timeframe).count()
        all_visits = sum((int(user_visit.visits) for user_visit in all_visitors))

        data = {
            'version': 1.0,
            'time': timezone.now(),
            'recent_visitors': recent_visitors,
            'all_visitors': all_visitors.count(),
            'all_visits': all_visits,
        }
        return Response(data)
