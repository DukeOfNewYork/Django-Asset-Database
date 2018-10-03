from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import AssetForm, LoginForm, AdministrationForm
from .models import Asset, Building, WeekOf
from datetime import datetime as dt
from datetime import timedelta as td
from .view_functions import format_csv
from urllib.parse import unquote


# Create your views here.

def administration(request):
    buildings = Building.objects.all()
    form = AdministrationForm()
    return render(request, 'DjangoAssetManagement/administration.html', {'name': 'administration', 'form':form, 'buildings':buildings})

def index(request):
    name = 'Asset Manager'
    buildings = Building.objects.all()
    locations = []
    for i in buildings:
        locations.append(i)
    if 'r' in request.GET and request.GET['r'] and 'l' in request.GET and request.GET['l']:
        room = request.GET['r']
        location = request.GET['l']
        form = AssetForm(initial={'room': room, 'location': Building.objects.get(name=location)})
    elif 'n' in request.GET and request.GET['n']:
        name = request.GET['n']
        form = AssetForm(initial={'name': name})
    else:
        form = AssetForm()
    return render(request, 'DjangoAssetManagement/index.html', {'name': name, 'form': form, 'locations': locations})


def building_list(request, building_query):
    """
    Takes any string from the browser and searches for the building with that name.
    :param building_query: the URL past /building/ does not parse spaces.
    :return: All assets within the building.
    """
    name = building_query
    try:
        buildings = Building.objects.get(name=building_query)
    except Building.DoesNotExist:
        return render(request, 'DjangoAssetManagement/building_list.html',
                      {'name': 'No Building Found', 'building': 'No Building Found', 'assets': [],
                       'num_of_assets': '0'})
    assets = []
    for a in buildings.Asset.all():
        assets.append(a)
    assets.sort(key=lambda x: (x.room, x.pub_date), reverse=True)
    return render(request, 'DjangoAssetManagement/building_list.html',
                  {'name': name, 'building': name, 'assets': assets, 'number_of_assets': len(assets)})


def all_assets(request):
    """
    Displays a list of all assets with their buildings, rooms, and weeks.
    """
    name = "List of All Assets"
    asset_list = []
    assets = Asset.objects.all()
    for f in assets:
        asset_list.append(f)
    asset_list.sort(key=lambda x: (x.location.name, x.room, x.pub_date), reverse=True)
    return render(request, 'DjangoAssetManagement/all-assets.html', {'name': name, 'assets': asset_list,
                                                                     'number_of_assets': len(assets)})


def all_weeks(request):
    """
    A list of weeks in order from newest to oldest
    """
    name = "All Weeks"
    week_list = []
    for f in WeekOf.objects.all():
        week_list.append(f)
    week_list.sort(key=lambda x: x.name, reverse=True)
    return render(request, 'DjangoAssetManagement/all_weeks.html',
                  {'name': name, 'num_weeks': len(week_list), 'week_list': week_list})


def week_of_list(request, select_week):
    """
    Takes any string from the browser and searches for the weeks with that name.
    :param select_week: the URL past /all_weeks/ does not parse spaces.
    :return: All assets of the week
    """
    name = "Week Of " + select_week
    assets = []
    try:
        week = WeekOf.objects.get(name=select_week)
    except WeekOf.DoesNotExist:
        return render(request, 'DjangoAssetManagement/week_of_list.html',
                      {'name': "No Date Found", "select_week": "No Date Found", 'assets': "", 'buildings': "",
                       'moves': ""})
    for f in week.Asset.all():
        assets.append(f)
        assets.sort(key=lambda x: (x.location.name, x.room, x.pub_date), reverse=True)
    return render(request, 'DjangoAssetManagement/week_of_list.html',
                  {'name': name, "select_week": select_week, 'select_week': select_week, 'assets': assets,
                   'number_of_assets': len(assets)})


def export_week(request, select_week):
    """
    Creates a CSV document from the assets of the selected week
    :param select_week: the URL parameter, does not parse spaces.
    :return: A CSV
    """
    try:
        selected_week = WeekOf.objects.get(name=select_week)
    except WeekOf.DoesNotExist:
        return render(request, 'DjangoAssetManagement/week_of_list.html',
                      {'name': "No Date Found", "select_week": "No Date Found", 'assets': "", 'buildings': "",
                       'moves': ""})
    week_assets = []
    for asset in selected_week.Asset.all():
        week_assets.append(asset)
    week_assets.sort(key=lambda x: (x.location.name, x.room, x.pub_date), reverse=True)
    return format_csv(week_assets, select_week)


def export_moves(request):
    """
    Creates a CSV document from the entire database.
    :return: A CSV
    """
    assets = []
    assets_object = Asset.objects.all()
    for asset in assets_object:
        assets.append(asset)
    return format_csv(assets, 'all_assets_exported')


def add_assets(request):
    """
    Takes the input form, attaches it to a week object, and saves it to the database.
    """
    # Generates the week, then the try except checks to see if it needs to create a new week object.
    this_week = (dt.today() - td(days=dt.today().isoweekday() % 7)).strftime('%Y-%m-%d')
    form = AssetForm(request.POST, request.FILES)
    try:
        week_object = WeekOf.objects.get(name=this_week)
    except WeekOf.DoesNotExist:
        week_object = WeekOf(name=this_week)
        week_object.save()
    if request.method == 'POST':
        if form.is_valid():
            asset = Asset(name=form.cleaned_data['name'], location=form.cleaned_data['location'],
                          room=form.cleaned_data['room'], image=form.cleaned_data['image'], week_of=week_object,
                          user=request.user)
            try:
                getAsset = Asset.objects.get(name=asset.name)
                getAsset.location = asset.location
                getAsset.room = asset.room
                getAsset.image = asset.image
                getAsset.week_of = week_object
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
    
def add_building(request):
    form = AdministrationForm(request.POST)
    print(form.cleaned_data['name'])
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    
def remove_building(request):
    if 'b' in request.GET and request.GET['b']:
        building = Building.objects.get(name=unquote(request.GET['b']))
        print(building)
        building.delete()
    return HttpResponseRedirect('/')


def image_upload(request):
    name = 'Image Upload'
    return render(request, 'DjangoAssetManagement/image_upload.html', {'name': name})


def image_scan(request):
    name = 'Image Scan'
    return render(request, 'DjangoAssetManagement/imagescan.html', {'name': name})

def upload_csv(request):
    this_week = (dt.today() - td(days=dt.today().isoweekday() % 7)).strftime('%Y-%m-%d')
    data = {}
    location_object = ''
#     try:
    csv_file = request.FILES["csv_file"] 
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return administration(request)
        #if file is too large, return
    if csv_file.multiple_chunks():
        messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        return administration(request)
    file_data = csv_file.read().decode("utf-8")        
 
    lines = file_data.split("\n")
        #loop over the lines and save them in db. If error , store as string and then display
    for line in lines:
        data = [x.strip() for x in line.split(',')]
        try:
            week_object = WeekOf.objects.get(name=this_week)
        except WeekOf.DoesNotExist:
            week_object = WeekOf(name=this_week)
            week_object.save()
        try:
            location_object = Building.objects.get(name=data[0])
        except Exception as e:
            location_object = Building(name=data[0])
            location_object.save()
        if True:
            asset = Asset(name=data[1], location=location_object, room=data[2], image='', week_of=week_object, user=request.user)
            print(asset)
        try:
            getAsset = Asset.objects.get(name=asset.name)
            getAsset.location = asset.location
            getAsset.room = asset.room
            getAsset.image = asset.image
            getAsset.week_of = week_object
            getAsset.save()
        except Asset.DoesNotExist:
            asset.save()
#             fields = line.split(",")
#             print(fields)
#             data_dict = {}
#             data_dict["location"] = fields[0]
#             data_dict["name"] = fields[1]
#             data_dict["room"] = fields[2]
#             data_dict["pub_date"] = dt.strptime(fields[3], '%m/%d/%Y %H:%M')
#             print(data_dict)
#             try:
#                 form = AssetForm(data_dict)
#                 if form.is_valid():
#                     form.save()
#                     print('form saved')
#                 else:
#                     print("Unable to save form. ")
#             except Exception as e:
#                 pass
#     except Exception as e:
#         print("Unable to upload file. ")
#         print(e)
#         print('error')
    return administration(request)


def profile(request, username):
    user = User.objects.get(username=username)
    assets = Asset.objects.get(user=user)
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
