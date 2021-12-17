# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from game.models import Games
#
# @api_view(['GET', 'POST'])
# def compareTwo(request):
#     if request.method == 'POST':
#         try:
#             game1 = request.data['game1']
#             game2 = request.data['game2']
#             data1 = Games.objects.using('game_db').filter(Name__icontains=game1).values_list(
#                 'Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales').distinct()[:1]
#             data2 = Games.objects.using('game_db').filter(Name__icontains=game2).values_list(
#                 'Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales').distinct()[:1]
#
#             data = [{
#                 "Name": data1[0][0],
#                 "NA_Sales": data1[0][1],
#                 "EU_Sales": data1[0][2],
#                 "JP_Sales": data1[0][3],
#                 "Other_Sales": data1[0][4],
#                 "Global_Sales": data1[0][5],
#
#             }, {
#                 "Name": data2[0][0],
#                 "NA_Sales": data2[0][1],
#                 "EU_Sales": data2[0][2],
#                 "JP_Sales": data2[0][3],
#                 "Other_Sales": data2[0][4],
#                 "Global_Sales": data2[0][5],
#             }]
#
#             return Response({"compare": data}, status=status.HTTP_200_OK)
#         except:
#             return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#
# @api_view(['GET', 'POST'])
# def total(request):
#     if request.method == 'POST':
#         try:
#             year1 = int(request.data['year1'])
#             year2 = int(request.data['year2'])
#             years = Games.objects.using('game_db').filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
#             year = set(y[0] for y in years)
#             total = {}
#             for y in year:
#                     temp = 0;
#                     data = Games.objects.using('game_db').filter(Year=y).values_list('Name','Global_Sales', 'Platform').distinct()
#                     for d in data:
#                         temp += d[1]
#                     total[y] = temp
#
#             return Response({"total": total}, status=status.HTTP_200_OK)
#         except:
#             return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#
# @api_view(['GET', 'POST'])
# def twoCompany(request):
#     if request.method == 'POST':
#         try:
#             year1 = int(request.data['year1'])
#             year2 = int(request.data['year2'])
#             company1 = request.data['company1']
#             company2 = request.data['company2']
#             years = Games.objects.using('game_db').filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
#             year = set(y[0] for y in years)
#             total = {}
#             for y in year:
#                     temp1 = 0;
#                     temp2 = 0;
#                     data1 = Games.objects.using('game_db').filter(Year=y, Publisher__icontains=company1).values_list('Name','Global_Sales', 'Platform', 'Publisher').distinct()
#                     data2 = Games.objects.using('game_db').filter(Year=y, Publisher__icontains=company2).values_list('Name', 'Global_Sales', 'Platform', 'Publisher').distinct()
#                     for d1 in data1:
#                         temp1 += d1[1]
#                     for d2 in data2:
#                         temp2 += d2[1]
#                     data = [{
#                         "Publisher": data1[0][3],
#                         "total": temp1,
#                     },{
#                         "Publisher": data2[0][3],
#                         "total": temp2,
#                     }]
#                     total[y] = data
#
#             return Response({"compare": total}, status=status.HTTP_200_OK)
#         except:
#             return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#
# @api_view(['GET', 'POST'])
# def compareGenre(request):
#     if request.method == 'POST':
#         try:
#             year1 = int(request.data['year1'])
#             year2 = int(request.data['year2'])
#             years = Games.objects.using('game_db').filter(Year__gte=year1, Year__lte=year2).values_list('Year').distinct()
#             genres = Games.objects.using('game_db').values_list('Genre').distinct()
#             year = set(y[0] for y in years)
#             genre = set(g[0] for g in genres)
#             total = {}
#             for g in genre:
#                 for y in year:
#                         temp = 0;
#                         data = Games.objects.using('game_db').filter(Year=y, Genre=g).values_list('Name', 'Global_Sales', 'Platform').distinct()
#                         for d in data:
#                             temp += d[1]
#
#                 data = [{
#                     "total": temp,
#                 }]
#                 total[g] = data
#
#             return Response({"compare genre": total}, status=status.HTTP_200_OK)
#         except:
#             return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
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

            labels = [data1[0][0], data2[0][0]]
            NA_Sales = [data1[0][1], data2[0][1]]
            EU_Sales= [data1[0][2], data2[0][2]]
            JP_Sales= [data1[0][3], data2[0][3]]
            Other_Sales= [data1[0][4], data2[0][4]]
            Global_Sales= [data1[0][5], data2[0][5]]

            x = np.arange(len(labels))  # the label locations
            width = 0.1  # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(x - 2*width, NA_Sales, width, label='NA_Sales')
            rects2 = ax.bar(x - width, EU_Sales, width, label='EU_Sales')
            rects3 = ax.bar(x , JP_Sales, width, label='JP_Sales')
            rects4 = ax.bar(x + width, Other_Sales, width, label='Other_Sales')
            rects5 = ax.bar(x + 2*width, Global_Sales, width, label='Global_Sales')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('sales')
            ax.set_title('compare sales')
            ax.set_xticks(x, labels)
            ax.legend()

            ax.bar_label(rects1, padding=3)
            ax.bar_label(rects2, padding=3)
            ax.bar_label(rects3, padding=3)
            ax.bar_label(rects4, padding=3)
            ax.bar_label(rects5, padding=3)

            # fig.tight_layout()
            canvas = FigureCanvasAgg(fig)
            response = HttpResponse(content_type = 'image/png')
            canvas.print_png(response)
            return response
            # return Response({"compare": data}, status=status.HTTP_200_OK)
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

            year = list(total.keys())
            values = list(total.values())
            fig = plt.figure(figsize = (10, 5))
            # creating the bar plot
            plt.bar(year, values, color ='maroon',
                    width = 0.4)
            plt.xlabel("years")
            plt.ylabel("sales")
            plt.title("compare sales year")
            canvas = FigureCanvasAgg(fig)
            response = HttpResponse(content_type = 'image/png')
            canvas.print_png(response)
            return response
            # return Response({"total": total}, status=status.HTTP_200_OK)
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

            Publisher1 = []
            Publisher2 = []

            for y in year:
                temp1 = 0;
                temp2 = 0;
                data1 = Games.objects.using('game_db').filter(Year=y, Publisher__icontains=company1).values_list('Name','Global_Sales', 'Platform', 'Publisher').distinct()
                data2 = Games.objects.using('game_db').filter(Year=y, Publisher__icontains=company2).values_list('Name', 'Global_Sales', 'Platform', 'Publisher').distinct()
                for d1 in data1:
                    temp1 += d1[1]
                for d2 in data2:
                    temp2 += d2[1]

                Publisher1.append(float(temp1))
                Publisher2.append(float(temp2))

                data = [{
                    "Publisher": data1[0][3],
                    "total": temp1,
                },{
                    "Publisher": data2[0][3],
                    "total": temp2,
                }]
                total[y] = data

            year = list(year)
            fig, ax = plt.subplots()
            ax.plot(year, Publisher1, label=data1[0][3])
            ax.plot(year, Publisher2, label=data2[0][3])
            ax.legend()
            canvas = FigureCanvasAgg(fig)
            response = HttpResponse(content_type = 'image/png')
            canvas.print_png(response)
            return response
            # return Response({"compare": total}, status=status.HTTP_200_OK)
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

                total[g] = temp
            #charr bar
            genre_ = list(total.keys())
            values = list(total.values())
            fig = plt.figure(figsize = (10, 5))
            # creating the bar plot
            plt.bar(genre_, values, color ='maroon',
                    width = 0.4)
            plt.xlabel("genre")
            plt.xticks(rotation=90)
            plt.ylabel("sales")
            plt.title("compare sales genres")
            canvas = FigureCanvasAgg(fig)
            response = HttpResponse(content_type = 'image/png')
            canvas.print_png(response)
            return response
            # return Response({"compare genre": total}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "method isn't post"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)