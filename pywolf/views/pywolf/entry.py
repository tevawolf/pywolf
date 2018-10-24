from ...models.pywolf.transactions import VillageParticipant

def entry(request, village_no, day_no):
    participant = VillageParticipant()
    participant.description = request.POST['description']

    pass