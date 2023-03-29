from django.shortcuts import render
from .models import AnnouncedPuResults, PollingUnit, Ward, Lga
from django.db.models import Sum
# Create your views here.

def dashboard(request):
    labels = []
    data = []
    party_votes = []
    
    party_scores = AnnouncedPuResults.get_party_scores().order_by('-total_score')
    for party in party_scores:
        labels.append(party['party_abbreviation'])
        data.append(party['total_score'])
        party_votes.append({'party_abbreviation': party['party_abbreviation'], 'total_score': party['total_score'], })
    
    # get all announced result so I can use it in HTML table 
    announcedpuresult = AnnouncedPuResults.objects.all()

    # This code uses the aggregate() function to calculate the sum of the total_voters field
    # for all instances of the AnnouncedPuResults model, and then extracts the result using the 
    # dictionary key 'total_voters__sum'.
    total_vote = AnnouncedPuResults.objects.aggregate(Sum('party_score'))['party_score__sum']

    # This code uses the values() and distinct() functions to get a list of distinct 
    # party_abbreviation values from all instances of the AnnouncedPuResults model, and then counts the 
    # number of distinct values using the count() function
    total_parties_announced = AnnouncedPuResults.objects.values('party_abbreviation').distinct().count()

    contex = {
        'announcedpuresult': announcedpuresult,
        'labels': labels,
        'data': data,
        'party_votes': party_votes,
        'total_vote': total_vote,
        'total_parties_announced': total_parties_announced
    }
    
    return render(request, "app/index.html", contex)

def unit_list(request):
    units = AnnouncedPuResults.objects.values_list('polling_unit_uniqueid', flat=True).distinct()
    context = {'units': units}
    return render(request, 'app/unit_list.html', context)

def polling_unit_results(request, uniqueid):
    labels = []
    data = []
    party_votes = []
    parties = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=uniqueid).order_by('-party_score')
    for party in parties:
        labels.append(party.party_abbreviation)
        data.append(party.party_score)
        party_votes.append({'party_abbreviation': party.party_abbreviation, 'party_score': party.party_score, })

    polling_unit_info = PollingUnit.objects.get(uniqueid=uniqueid)
    
    total_parties_announced = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=uniqueid).count()
    total_vote = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=uniqueid).aggregate(Sum('party_score'))['party_score__sum']
    context = {
        'party_votes': party_votes, 
        'uniqueid': uniqueid, 
        'labels': labels, 
        'data': data, 
        'total_parties_announced': total_parties_announced, 
        'total_vote': total_vote,
        'polling_unit_info': polling_unit_info,
        }
    return render(request, 'app/polling_unit_results.html', context)

