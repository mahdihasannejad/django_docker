from django.shortcuts import render
from game.models import Games
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import os
import csv
from django.http import JsonResponse


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        g = os.path.exists("C:/mehti/project/Django/cloud/game/vgsales.csv")
        file = open("C:/mehti/project/Django/cloud_test/game/vgsales.csv")
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            if row[3] == 'N/A':
                row[3] = 0
            rows.append(row)

        for i in range(1,len(rows)):
            b = Games(Rank=float(rows[i][0]),Name=rows[i][1],Platform = rows[i][2],Year = float(rows[i][3]) ,Genre =rows[i][4],
                Publisher=rows[i][5],NA_Sales=float(rows[i][6]),EU_Sales=float(rows[i][7]),JP_Sales=float(rows[i][8]),
                Other_Sales = float(rows[i][9]),Global_Sales =float(rows[i][10]))
            b.save()
        return Response({"Post.": "succsus"})
    Games.objects.all().delete()
    return Response({"Hello, world. You're at the polls index."})

@api_view(['GET', 'POST'])
def topplatform(request):
    if request.method == 'POST':
        topN = int(request.data['N'])
        platforms =Games.objects.values_list('Platform')

        set_platform = set(platform[0] for platform in platforms)
        a = {}
        for platform in set_platform:
            a[platform] = (Games.objects.filter(Platform=platform).order_by('-Global_Sales').values_list('Name','Global_Sales')[0:topN])
        return Response(a)
    return Response({'error':"request not post"})

@api_view(['GET', 'POST'])
def ir_rank(request):
    if request.method == 'POST':
        return Response({'Rank': request.data['Rank']})
    return Response({'error':"request not post"})

@api_view(['GET', 'POST'])
def ir_name(request):
    if request.method == 'POST':
        return Response({'Rank': request.data['Name']})
    return Response({'error':"request not post"})

@api_view(['GET', 'POST'])
def topYear(request):
    if request.method == 'POST':
        return Response({'N': request.data['N']})
    return Response({'error':"request not post"})

@api_view(['GET', 'POST'])
def topCategory(request):
    if request.method == 'POST':
        return Response({'N': request.data['N']})
    return Response({'error':"request not post"})

@api_view(['GET', 'POST'])
def topYear_platform(request):
    if request.method == 'POST':
        return Response({'Year': request.data['Year'],'Platform':request.data['Platform']})
    return Response({'error':"request not post"})

@api_view(['GET'])
def topEU_NAm(request):
    return Response({'topEU'})