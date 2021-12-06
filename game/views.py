from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
import os
import csv
from django.http import JsonResponse


@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        try:
            file = open("vgsales.csv")
            csvreader = csv.reader(file)
            rows = []
            for row in csvreader:
                if row[3] == 'N/A':
                    row[3] = 0
                rows.append(row)

            for i in range(1, len(rows)):
                b = Games(Rank=float(rows[i][0]), Name=rows[i][1], Platform=rows[i][2], Year=float(rows[i][3]),
                          Genre=rows[i][4],
                          Publisher=rows[i][5], NA_Sales=float(rows[i][6]), EU_Sales=float(rows[i][7]),
                          JP_Sales=float(rows[i][8]),
                          Other_Sales=float(rows[i][9]), Global_Sales=float(rows[i][10]))
                b.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed to add csv file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    Games.objects.all().delete()
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def rank(request):
    if request.method == 'POST':
        try:
            game_rank = request.data['rank']
            game = Games.objects.filter(Rank=game_rank)
            data = [{
                "Rank": game[0].Rank,
                "Name": game[0].Name,
                "Platform": game[0].Platform,
                "Year": game[0].Year,
                "Genre": game[0].Genre,
                "Publisher": game[0].Publisher,
                "NA_Sales": game[0].NA_Sales,
                "EU_Sales": game[0].EU_Sales,
                "JP_Sales": game[0].JP_Sales,
                "Other_Sales": game[0].Other_Sales,
                "Global_Sales": game[0].Global_Sales, }]
            return Response({"game": data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def name(request):
    if request.method == 'POST':
        try:
            game_name = request.data['name']
            games = Games.objects.filter(Name__icontains=game_name).values_list(
                "Rank", "Name", "Platform", "Year", "Genre", "Publisher", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"
            ).distinct()
            data = []
            for g in games:
                data.append({
                    "Rank": g[0],
                    "Name": g[1],
                    "Platform": g[2],
                    "Year": g[3],
                    "Genre": g[4],
                    "Publisher": g[5],
                    "NA_Sales": g[6],
                    "EU_Sales": g[7],
                    "JP_Sales": g[8],
                    "Other_Sales": g[9],
                    "Global_Sales": g[10],
                })
            return Response({"games": data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def topPlatform(request):
    if request.method == 'POST':
        try:
            topN = int(request.data['N'])
            platforms = Games.objects.values_list('Platform').distinct()
            set_platform = set(platform[0] for platform in platforms)
            a = {}
            for platform in set_platform:
                a[platform] = (
                    Games.objects.filter(Platform=platform).order_by('-Global_Sales').values_list('Name').distinct()[
                    :topN])
            return Response(a, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def topYear(request):
    if request.method == 'POST':
        try:
            topN = int(request.data['N'])
            years = Games.objects.values_list('Year').distinct()
            set_year = set(year[0] for year in years)
            a = {}
            for year in set_year:
                if year != 0:
                    a[year] = (
                        Games.objects.filter(Year=year).order_by('-Global_Sales').values_list('Name').distinct()[:topN])
            return Response(a, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def topGenre(request):
    if request.method == 'POST':
        try:
            topN = int(request.data['N'])
            genres = Games.objects.values_list('Genre').distinct()
            a = {}
            set_genre = set(genre[0] for genre in genres)
            for genre in set_genre:
                a[genre] = (
                    Games.objects.filter(Genre=genre).order_by('-Global_Sales').values_list('Name').distinct()[:topN])
            return Response(a, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def topYearPlatform(request):
    if request.method == 'POST':
        try:
            year = int(request.data['year'])
            platform = request.data['platform']
            data = Games.objects.filter(
                Year=year, Platform__icontains=platform).order_by('-Global_Sales').values_list('Name', 'Year',
                                                                                               'Platform').distinct()[
                   :5]
            return Response({"top 5": data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def naLessThanEU(request):
    if request.method == 'POST':
        try:
            data1 = Games.objects.order_by('-Global_Sales').values_list('Name', 'EU_Sales', 'NA_Sales', 'Platform').distinct()
            data = []
            for i in range(len(data1)):
                if data1[i][1] > data1[i][2]:
                    temp = [data1[i][0], data1[i][3]]
                    data.append(temp)
            return Response({"games": data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
def compareTwo(request):
    if request.method == 'POST':
        try:
            game1 = request.data['game1']
            game2 = request.data['game2']
            data1 = Games.objects.filter(Name__icontains=game1).values_list(
                'Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales').distinct()[:1]
            data2 = Games.objects.filter(Name__icontains=game2).values_list(
                'Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales').distinct()[:1]

            data = [{
                "Name": data1[0][0],
                "NA_Sales": data1[0][1],
                "EU_Sales": data1[0][2],
                "JP_Sales": data1[0][3],
                "Other_Sales": data1[0][4],
                "Global_Sales": data1[0][5],

            }, {
                "Name": data2[0][0],
                "NA_Sales": data2[0][1],
                "EU_Sales": data2[0][2],
                "JP_Sales": data2[0][3],
                "Other_Sales": data2[0][4],
                "Global_Sales": data2[0][5],
            }]

            return Response({"compare": data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def total(request):
    if request.method == 'POST':
        try:
            year1 = int(request.data['year1'])
            year2 = int(request.data['year2'])
            years = Games.objects.filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
            year = set(y[0] for y in years)
            total = {}
            for y in year:
                    temp = 0;
                    data = Games.objects.filter(Year=y).values_list('Name','Global_Sales', 'Platform').distinct()
                    for d in data:
                        temp += d[1]
                    total[y] = temp

            return Response({"total": total}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def twoCompany(request):
    if request.method == 'POST':
        try:
            year1 = int(request.data['year1'])
            year2 = int(request.data['year2'])
            company1 = request.data['company1']
            company2 = request.data['company2']
            years = Games.objects.filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
            year = set(y[0] for y in years)
            total = {}
            for y in year:
                    temp1 = 0;
                    temp2 = 0;
                    data1 = Games.objects.filter(Year=y, Publisher__icontains=company1).values_list('Name','Global_Sales', 'Platform', 'Publisher').distinct()
                    data2 = Games.objects.filter(Year=y, Publisher__icontains=company2).values_list('Name', 'Global_Sales', 'Platform', 'Publisher').distinct()
                    for d1 in data1:
                        temp1 += d1[1]
                    for d2 in data2:
                        temp2 += d2[1]
                    data = [{
                        "Publisher": data1[0][3],
                        "total": temp1,
                    },{
                        "Publisher": data2[0][3],
                        "total": temp2,
                    }]
                    total[y] = data

            return Response({"compare": total}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def compareGenre(request):
    if request.method == 'POST':
        try:
            year1 = int(request.data['year1'])
            year2 = int(request.data['year2'])
            years = Games.objects.filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
            genres = Games.objects.values_list('Genre').distinct()
            year = set(y[0] for y in years)
            genre = set(g[0] for g in genres)
            total = {}
            for g in genre:
                for y in year:
                        temp = 0;
                        data = Games.objects.filter(Year=y, Genre=g).values_list('Name', 'Global_Sales', 'Platform').distinct()
                        for d in data:
                            temp += d[1]

                data = [{
                    "total": temp,
                }]
                total[g] = data

            return Response({"compare genre": total}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)