import json

import numpy as np
import requests
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.utils.encoding import smart_str

from TMSFreshStart import settings
from branch_and_bound import BranchAndBound
from knn import nearestNeighbor
from .forms import UploadFileForm
import pandas as pd
from django.http import HttpResponse

# Create your views here.
def setup_view(request,*args,**kwargs):
    try:
        locations,method=getDataFromForm(request)
        distance_data=getDistances(locations)
        distance_matrix=createDistanceMatrix(locations,distance_data)
        ordered_locations=constructRoute(locations,distance_matrix,method)
        ordered_locations_to_print=[i[:-6] for i in ordered_locations]
    except:
        ordered_locations_to_print=''
        ordered_locations=[]
        method=''
        status=[]
    return render(request, "setup.html",
                  {'cities': ordered_locations_to_print, 'api_key': settings.API_KEY, 'json': json.dumps(ordered_locations),
                   'method': method})


def removeChar(s, c=','):
    counts = s.count(c)
    s = list(s)
    while counts:
        s.remove(c)
        counts -= 1
    s = ''.join(s)
    return s


# Catches input of form and prepares the necessary data
def getDataFromForm(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # Use pandas to get cities names
        df = pd.read_csv(request.FILES['document'])
        if len(df.columns)==1:
            method = request.POST['methodd']
            locations = df.villes.tolist()
            locations = [i + " Maroc" for i in df.villes.tolist()[0:min(10, len(locations))]]
        return locations,method


# Get distance data from API
def getDistances(cities):
    # Make url for distance matrix
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
    for city in cities:
        url += city
        url += "|"
    url = url[:-1]
    url += "&destinations="
    for city in cities:
        url += city
        url += "|"
    url = url[:-1]
    url += "&units=metric&key=" + settings.API_KEY
    # Send request and store response as JSON
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data


# Create distance matrix
def createDistanceMatrix(cities,data):
    l = []
    ll = []
    for i in range(len(cities)):
        for j in range(len(cities)):
            distance = data['rows'][i]['elements'][j]['distance']['value']
            if distance == 0: distance = np.inf
            ll.append(distance)
        l.append(ll)
        ll = []
    matrix = np.array(l)
    return matrix


def knn(cities,matrix):
    knn_output = nearestNeighbor(matrix, 0)
    ordered_cities = []
    for i in knn_output:
        ordered_cities.append((smart_str(cities[i - 1])))
    return ordered_cities
def branchBound(cities,matrix):
    agent = BranchAndBound(matrix)
    agent.TSP()
    ordered_cities=[]
    bb_output = agent.final_path
    for i in bb_output:
        ordered_cities.append((smart_str(cities[i])))
    return ordered_cities

def constructRoute(cities,matrix,method):
    if method=='Mode rapide':
        return knn(cities,matrix)
    elif method=='Mode avancé':
        return branchBound(cities,matrix)