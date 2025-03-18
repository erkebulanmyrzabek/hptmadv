from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import HackathonPrizePlace

@receiver(m2m_changed, sender=HackathonPrizePlace.winner_teams.through)
def award_winners(sender, instance, action, **kwargs):
    if action == "post_add":
        for team in instance.winner_teams.all():
            for member in team.members.all():
                member.xp += instance.xp_reward
                member.balance += instance.prize_amount or 0
                member.save()