from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from donnee.models import Vote, Candidat

def notify_vote_update(election):
    channel_layer = get_channel_layer()

    candidats = Candidat.objects.filter(election=election)

    data = []
    total_votes = 0

    for c in candidats:
        votes = c.total_votes()
        total_votes += votes
        data.append({
            "id": c.id,
            "name": c.nom_complet,  # <-- ici on aligne avec le JS
            "votes": votes
        })

    data = sorted(data, key=lambda x: x["votes"], reverse=True)

    async_to_sync(channel_layer.group_send)(
        "votes_dashboard",
        {
            "type": "send_vote_update",
            "data": {
                "type": "votes_update",
                "total_votes": total_votes,
                "candidats": data,
            }
        }
    )