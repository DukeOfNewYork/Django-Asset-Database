# from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import AssetForm, LoginForm
from .models import Asset, Building, WeekOf
from datetime import datetime as dt
from datetime import timedelta as td
import csv


# Create your views here.
# listo = []


def index(request):
    buildings = Building.objects.all()
    listo = []
    name = 'Asset Manager'
    if 'r' in request.GET and request.GET['r'] and 'l' in request.GET and request.GET['l']:
        room = request.GET['r']
        location = request.GET['l']
        form = AssetForm(initial={'room': room, 'location': Building.objects.get(name=location)})
    elif 'n' in request.GET and request.GET['n']:
        name = request.GET['n']
        form = AssetForm(initial={'name': name})
    else:
        form = AssetForm()
    for i in buildings:
        listo.append(i)
    return render(request, 'DjangoAssetManagement/index.html', {'name': name, 'form': form, 'locations': listo})


def building_list(request, buildingI):
    buildings = Building.objects.all()
    try:
        buildings = Building.objects.get(name=buildingI)
    except Building.DoesNotExist:
        return render(request, 'DjangoAssetManagement/building_list.html',
                      {'name': 'No Building Found', 'building': 'No Building Found', 'assets': [],
                       'num_of_assets': '0'})
    name = buildingI
    listo = []
    for f in buildings.Asset.all():
        listo.append(f)
    listo.sort(key=lambda x: (x.room, x.pub_date), reverse=True)
    num_of_assets = len(listo)
    return render(request, 'DjangoAssetManagement/building_list.html',
                  {'name': name, 'building': name, 'assets': listo, 'num_of_assets': num_of_assets})


def all_assets(request):
    name = "List of All Assets"
    asset_list = []
    assets = Asset.objects.all()
    for f in assets:
        asset_list.append(f)
        asset_list.sort(key=lambda x: (x.location.name, x.room, x.pub_date), reverse=True)
    moves = len(assets)
    return render(request, 'DjangoAssetManagement/all-assets.html', {'name': name, 'assets': asset_list, 'moves': moves})


def all_weeks(request):
    name = "All Weeks"
    week_list = []
    for f in WeekOf.objects.all():
        week_list.append(f)
    num_weeks = len(week_list)
    return render(request, 'DjangoAssetManagement/all_weeks.html', {'name': name, 'num_weeks': num_weeks, 'week_list': week_list})


def week_of_list(request, select_week):
    try:
        weekobj = WeekOf.objects.get(name=select_week)
    except WeekOf.DoesNotExist:
        return render(request, 'DjangoAssetManagement/week_of_list.html',
                      {'name': "No Date Found", "select_week": "No Date Found", 'assets': "", 'buildings': "",
                       'moves': ""})
    name = "Week Of " + select_week
    lastRoom = 0
    aList = []
    for f in weekobj.Asset.all():
        aList.append(f)
    aList.sort(key=lambda x: (x.location.name, x.room, x.pub_date), reverse=True)
    moves = len(aList)
    return render(request, 'DjangoAssetManagement/week_of_list.html',
                  {'name': name, "select_week": select_week, 'select_week': select_week, 'assets': aList,
                   'moves': moves})


def export_week(request, select_week):
    lastLoc = ""
    lastRoom = ""
    try:
        weekobj = WeekOf.objects.get(name=select_week)
    except WeekOf.DoesNotExist:
        return render(request, 'DjangoAssetManagement/week_of_list.html',
                      {'name': "No Date Found", "select_week": "No Date Found", 'assets': "", 'buildings': "",
                       'moves': ""})
    listo = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    for asset in weekobj.Asset.all():
        listo.append(asset)
    listo.sort(key=lambda x: (x.location.name, x.room, x.pub_date), reverse=True)
    writer.writerow(["Week of " + select_week])
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
    last_loc = ""
    last_room = ""
    listo = []
    assets = Asset.objects.all()
    buildings = Building.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    for asset in assets:
        listo.append(asset)
    listo.sort(key=lambda x: (x.location.name, x.room), reverse=True)
    writer.writerow(["All stored Assets"])
    for x in listo:
        if last_loc != x.location:
            last_loc = x.location
            writer.writerow([""])
            writer.writerow([""])
            writer.writerow([x.location])
            writer.writerow([""])
        elif last_room != x.room:
            last_room = x.room
            writer.writerow([""])
        writer.writerow([x.name, x.room, ("{:%Y-%m-%d %H:%M}".format(x.pub_date))])
    return response


def add_assets(request):
    assets = Asset.objects.all()
    weeks = WeekOf.objects.all()
    thisweek = (dt.today() - td(days=dt.today().isoweekday() % 7)).strftime('%Y-%m-%d')
    form = AssetForm(request.POST, request.FILES)
    try:
        weekobj = WeekOf.objects.get(name=thisweek)
    except WeekOf.DoesNotExist:
        weekobj = WeekOf(name=thisweek)
        weekobj.save()
    if request.method == 'POST':
        if form.is_valid():
            asset = Asset(name=form.cleaned_data['name'], location=form.cleaned_data['location'],
                          room=form.cleaned_data['room'], image=form.cleaned_data['image'], week_of=weekobj,
                          user=request.user)
            try:
                getAsset = Asset.objects.get(name=asset.name)
                getAsset.location = asset.location
                getAsset.room = asset.room
                getAsset.image = asset.image
                getAsset.week_of = weekobj
                getAsset.save()
                return HttpResponseRedirect('/?r=' + asset.room + '&l=' + asset.location.name)
            except Asset.DoesNotExist:
                asset.save()
            return HttpResponseRedirect('/?r=' + asset.room + '&l=' + asset.location.name)
    else:
        return render(request, 'DjangoAssetManagement/index.html', {'form': form})


def add_image(request):
    form = AssetForm(request.POST, request.FILES)
    if form.is_valid():
        form.save(commit=True)
        return HttpResponseRedirect('/')


def image_upload(request):
    name = 'Image Upload'
    return render(request, 'DjangoAssetManagement/image_upload.html', {'name': name})


def image_scan(request):
    name = 'Image Scan'
    return render(request, 'DjangoAssetManagement/imagescan.html', {'name': name})


def profile(request, username):
    user = User.objects.get(username=username)
    assets = Asset.objects.filter(user=user)
    return render(request, 'DjangoAssetManagement/profile.html', {'name': username, 'assets': assets})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'DjangoAssetManagement/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
