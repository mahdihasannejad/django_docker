from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from game.models import Games

@api_view(['GET', 'POST'])
def compareTwo(request):
    if request.method == 'POST':
        try:
            game1 = request.data['game1']
            game2 = request.data['game2']
            data1 = Games.objects.using('game_db').filter(Name__icontains=game1).values_list(
                'Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales').distinct()[:1]
            data2 = Games.objects.using('game_db').filter(Name__icontains=game2).values_list(
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
            years = Games.objects.using('game_db').filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
            year = set(y[0] for y in years)
            total = {}
            for y in year:
                    temp = 0;
                    data = Games.objects.using('game_db').filter(Year=y).values_list('Name','Global_Sales', 'Platform').distinct()
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
            years = Games.objects.using('game_db').filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
            year = set(y[0] for y in years)
            total = {}
            for y in year:
                    temp1 = 0;
                    temp2 = 0;
                    data1 = Games.objects.using('game_db').filter(Year=y, Publisher__icontains=company1).values_list('Name','Global_Sales', 'Platform', 'Publisher').distinct()
                    data2 = Games.objects.using('game_db').filter(Year=y, Publisher__icontains=company2).values_list('Name', 'Global_Sales', 'Platform', 'Publisher').distinct()
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
            years = Games.objects.using('game_db').filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
            genres = Games.objects.using('game_db').values_list('Genre').distinct()
            year = set(y[0] for y in years)
            genre = set(g[0] for g in genres)
            total = {}
            for g in genre:
                for y in year:
                        temp = 0;
                        data = Games.objects.using('game_db').filter(Year=y, Genre=g).values_list('Name', 'Global_Sales', 'Platform').distinct()
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