from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import AssetForm
from .models import Asset, Building, WeekOf
from datetime import datetime as dt
from datetime import timedelta as td
import csv

listo = []

#The index contains the main form
def index(request):
    buildings = Building.objects.all()
    listo = []
    #The name changes what is displayed in the upper left of the web page
    name = 'Asset Manager'
    #Where R is room and L is location it checks the URL, and if it's there it auto fills the form fields
    if 'r' in request.GET and request.GET['r'] and 'l' in request.GET and request.GET['l']:
        r = request.GET['r']
        l = request.GET['l']
        form = AssetForm(initial={'room':r,'location':Building.objects.get(name=l)})
    #Where N is the asset name it auto fills the form name field
    elif 'n' in request.GET and request.GET['n']:
        n = request.GET['n']
        form = AssetForm(initial={'name':n})
    else:
        form = AssetForm()
    #listo is a list of buildings that are displayed at the bottom of the page as links to the building (building_list)
    for i in buildings:
        listo.append(i)
    return render(request, 'DjangoAssetManagement/index.html', {'name':name,'form': form,'locations':listo})

#The building list where it displays all assets assigned to that building for all time
def building_list(request, buildingI):
    buildings = Building.objects.all()
    try:
        buildings = Building.objects.get(name=buildingI)
    except Building.DoesNotExist:
        return render(request, 'DjangoAssetManagement/building_list.html', {'name':'No Building Found','building':'No Building Found','assets':[],'num_of_assets':'0'})  
    #The name changes what is displayed in the upper left of the web page
    name = buildingI
    listo=[]
    #Gathering all of the assets assigned to the building to be displayed
    for f in buildings.Asset.all():
        listo.append(f)
    listo.sort(key=lambda x: (x.room,x.pub_date), reverse=True)
    num_of_assets = len(listo)
    return render(request, 'DjangoAssetManagement/building_list.html', {'name':name,'building':name,'assets':listo,'num_of_assets':num_of_assets})

def all_assets(request):
    #The name changes what is displayed in the upper left of the web page
    name = "List of All Assets"
    listo = []
    assets = Asset.objects.all()
    for f in assets:
        listo.append(f)
    #After gathering all of the assets it sorts by location,room, then date.
    listo.sort(key=lambda x: (x.location.name,x.room,x.pub_date), reverse=True)
    moves = len(assets)
    return render(request, 'DjangoAssetManagement/all-assets.html', {'name':name,'assets':listo,'moves':moves})

def all_weeks(request):
    #The name changes what is displayed in the upper left of the web page
    name = "All Weeks"
    allWeeks =[]
    for f in WeekOf.objects.all():
        allWeeks.append(f)
    numWeeks = len(allWeeks)
    return render(request, 'DjangoAssetManagement/all_weeks.html', {'name':name,'numWeeks':numWeeks,'allWeeks':allWeeks})

def week_of_list(request, select_week):
    #The name changes what is displayed in the upper left of the web page
    name = "Week Of " + select_week
    #If the week exsists it is displayed, if not then a basic no date found page is displayed
    try:
        weekobj = WeekOf.objects.get(name=select_week)
    except WeekOf.DoesNotExist:
        return render(request, 'DjangoAssetManagement/week_of_list.html', {'name':"No Date Found","select_week":"No Date Found",'assets':"",'buildings':"",'moves':""})
    lastRoom = 0
    aList = []
    for f in weekobj.Asset.all():
        aList.append(f)
    aList.sort(key=lambda x: (x.location.name,x.room,x.pub_date), reverse=True)
    moves = len(aList)
    return render(request, 'DjangoAssetManagement/week_of_list.html', {'name':name,"select_week":select_week,'select_week':select_week,'assets':aList,'moves':moves})

def export_week(request,select_week):
    listo=[]
    #These two variables keep track of the last location and room
    lastLoc = ""
    lastRoom = ""
    try:
        weekobj = WeekOf.objects.get(name=select_week)
    except WeekOf.DoesNotExist:
        return render(request, 'DjangoAssetManagement/week_of_list.html', {'name':"No Date Found","select_week":"No Date Found",'assets':"",'buildings':"",'moves':""})
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    for asset in weekobj.Asset.all():
        listo.append(asset)
    listo.sort(key=lambda x: (x.location.name,x.room,x.pub_date), reverse=True)
    writer.writerow(["Week of " + select_week])
    #Checking for a change in building or room it will then add some space so it's easier 
    for x in listo:
        if lastLoc != x.location:
            lastLoc = x.location
            writer.writerow([""])
            writer.writerow([""])
            writer.writerow([x.location])
            writer.writerow([""])
        elif lastRoom != x.room:
            lastRoom = x.room
            writer.writerow([""])
        writer.writerow([x.name, x.room, ("{:%Y-%m-%d %H:%M}".format(x.pub_date))])
    return response

def export_moves(request):
    listo=[]
    #These two variables keep track of the last location and room
    lastLoc = ""
    lastRoom = ""
    assets = Asset.objects.all()
    buildings = Building.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    for asset in assets:
        listo.append(asset)
    listo.sort(key=lambda x: (x.location.name,x.room), reverse=True)
    writer.writerow(["All stored Assets"])
    #Checking for a change in building or room it will then add some space so it's easier
    for x in listo:
        if lastLoc != x.location:
            lastLoc = x.location
            writer.writerow([""])
            writer.writerow([""])
            writer.writerow([x.location])
            writer.writerow([""])
        elif lastRoom != x.room:
            lastRoom = x.room
            writer.writerow([""])
        writer.writerow([x.name, x.room, ("{:%Y-%m-%d %H:%M}".format(x.pub_date))])
    return response

def add_assets(request):
    #This is the process for adding assets to the database
    assets = Asset.objects.all()
    weeks = WeekOf.objects.all()
    #This process generates the name of the week
    thisweek = (dt.today() - td(days=dt.today().isoweekday() % 7)).strftime('%Y-%m-%d')
    form = AssetForm(request.POST,request.FILES)
    #Checking to see if the week already exsists and if it doesn't it makes it
    try:
        weekobj = WeekOf.objects.get(name=thisweek)
    except WeekOf.DoesNotExist:
        weekobj = WeekOf(name=thisweek)
        weekobj.save()
    if request.method == 'POST':
        if form.is_valid():
            asset = Asset(name = form.cleaned_data['name'],location = form.cleaned_data['location'],room = form.cleaned_data['room'],image = form.cleaned_data['image'],week_of=weekobj)
            try:
                getAsset = Asset.objects.get(name=asset.name)
                getAsset.location=asset.location
                getAsset.room=asset.room
                getAsset.image=asset.image
                getAsset.week_of=weekobj
                getAsset.save()
                return HttpResponseRedirect('/?r=' + asset.room + '&l=' + asset.location.name)
            except Asset.DoesNotExist:
                asset.save()
            return HttpResponseRedirect('/?r=' + asset.room + '&l=' + asset.location.name)
    else:
        return render(request, 'DjangoAssetManagement/index.html', {'form': form})

def add_image(request):
    #If a valid image is present it adds it to the database
    form = AssetForm(request.POST,request.FILES)
    if form.is_valid():
        form.save(commit = True)
        return HttpResponseRedirect('/')
