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
        status = 'fail'
        method=''
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            # Use pandas to get cities names
            df = pd.read_csv(request.FILES['document'])
            method=request.POST['methodd']
            cities=df.villes.tolist()
            cities = [i+" Maroc" for i in df.villes.tolist()[0:min(10,len(cities))]]

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
            url += "&units=metric&key="+settings.API_KEY
            # Send request and store response as JSON
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            data = json.loads(response.text)
            # Create distance matrix
            l = []
            ll = []
            for i in range(len(cities)):
                for j in range(len(cities)):
                    distance = data['rows'][i]['elements'][j]['distance']['value']
                    if distance == 0 : distance = np.inf
                    ll.append(distance)
                l.append(ll)
                ll = []
            matrix = np.array(l)
        ordered_cities = []
        if method=='Mode rapide':
            knn_output = nearestNeighbor(matrix, 0)
            ordered_cities = []
            for i in knn_output:
                ordered_cities.append((smart_str(cities[i - 1])))
        elif method=='Mode avancé':
            agent = BranchAndBound(matrix)
            agent.TSP()
            bb_output=agent.final_path
            for i in bb_output:
                ordered_cities.append((smart_str(cities[i] )))
        status='success'
        ordered_cities_to_print=[i[:-6] for i in ordered_cities]
        status=[status]
        return render(request,"setup.html",{'cities':ordered_cities_to_print,'api_key':settings.API_KEY,'json':json.dumps(ordered_cities),'method':method,'status':json.dumps(status)})
    except:
        pass

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
        method = request.POST['methodd']
        cities = df.villes.tolist()
        cities = [i + " Maroc" for i in df.villes.tolist()[0:min(10, len(cities))]]
        return cities,method
