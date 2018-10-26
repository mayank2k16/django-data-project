from django.shortcuts import render
from django.db.models import Count,Sum,Avg
from .models import Matches,Deliveries
from collections import OrderedDict
import json
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
def data_project_1(request):
        number_of_matches_per_season = list(Matches.objects.all().values('season').annotate(total = Count('season')).order_by('season'))
        return render(request, 'visualization/data1.html',{'dataset':number_of_matches_per_season})

def get_unique_years():
    unique_years = list()
    seasons = Matches.objects.values('season').distinct().order_by('season')
    for years in range(0,len(seasons)):
        unique_years.append(str(seasons[years]['season']))
    return unique_years
      
@cache_page(CACHE_TTL)
def data_project_2(request):
    team_names = OrderedDict()
    team_names = {'Sunrisers Hyderabad': [], 'Rising Pune Supergiants': [], 'Kolkata Knight Riders': [],'Kings XI Punjab': [],
                  'Royal Challengers Bangalore': [], 'Mumbai Indians': [], 'Delhi Daredevils': [], 'Gujarat Lions': [],
                  'Chennai Super Kings': [], 'Rajasthan Royals': [], 'Deccan Chargers': [], 'Kochi Tuskers Kerala': [], 'Pune Warriors': []}
    unique_years = get_unique_years()
    for team in team_names:
        number_of_winnings_per_year = []
        for year in unique_years:
            winnings_per_team_per_year=list(Matches.objects.all().values('winner').annotate(total_wins = Count('winner')).filter(season=year).filter(winner=team))
            if winnings_per_team_per_year:
                number_of_winnings_per_year.append((winnings_per_team_per_year[0]['total_wins']))
            else:
                number_of_winnings_per_year.append(0)
        team_names[team] = number_of_winnings_per_year
    return render(request,'visualization/data2.html',{'years':unique_years,'teams':team_names})

@cache_page(CACHE_TTL)
def data_project_3(request):
    matches_of_2016 = Matches.objects.only("season","id").filter(season=2016)
    teams  = list(Deliveries.objects.only("match_id","bowling_team","extra_runs").filter(match_id__in=matches_of_2016).only("bowling_team").values("bowling_team").annotate(runs = Sum("extra_runs")))
    return render(request,'visualization/data3.html',{'teams':teams})

@cache_page(CACHE_TTL)
def data_project_4(request):
    matches_of_2015 = Matches.objects.only("season", "id").filter(season=2015)
    most_economical_bowlers = list(Deliveries.objects.filter(match_id__in=matches_of_2015).values("bowler").annotate(avg = Avg("total_runs")*6).order_by('avg')[:10])
    return render(request,'visualization/data4.html',{'most_economical_bowlers':most_economical_bowlers})

@cache_page(CACHE_TTL)
def data_project_5(request):
    most_valuable_players = list(Matches.objects.all().values('player_of_match').annotate(total = Count('player_of_match')).order_by('-total'))[:10]
    return render(request, 'visualization/data5.html',{'mvp':most_valuable_players})
