from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.events.models import Hackathon
from .serializers import OrganizerHackathonSerializer
from django.http import HttpResponse
import csv

class OrganizerHackathonViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizerHackathonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hackathon.objects.filter(organization__id=self.request.user.organization_id)  # Предполагается связь с организацией

    @action(detail=True, methods=['post'])
    def announce_results(self, request, pk=None):
        hackathon = self.get_object()
        if hackathon.status != 'finished':
            return Response({"detail": "Хакатон ещё не завершён"}, status=status.HTTP_400_BAD_REQUEST)
        results = request.data.get('results', [])  # [{'place': 1, 'team_id': 1}, ...]
        for result in results:
            prize = hackathon.hackathon_prizes.filter(place=result['place']).first()
            if prize:
                prize.winner_teams.add(result['team_id'])
        hackathon.status = 'results_announced'
        hackathon.save()
        return Response({"detail": "Результаты объявлены"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def download_results(self, request, pk=None):
        hackathon = self.get_object()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="hackathon_{hackathon.id}_results.csv"'
        writer = csv.writer(response)
        writer.writerow(['Team', 'Place', 'Prize', 'XP'])
        for prize in hackathon.hackathon_prizes.all():
            for team in prize.winner_teams.all():
                writer.writerow([team.name, prize.place, prize.prize_amount, prize.xp_reward])
        return response