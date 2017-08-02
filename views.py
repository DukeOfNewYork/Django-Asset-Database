from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import AssetForm
from .models import Asset, Building
import csv
# Create your views here.

def index(request):
    name = 'Asset Manager'
    form = AssetForm()
    for i in assets:
        if i.location not in listo:
            listo.append(i.location)
    return render(request, 'DjangoAssetManagement/index.html', {'name':name,'form': form,'locations':listo})

def add_image(request):
    form = AssetForm(request.POST,request.FILES)
    if form.is_valid():
        form.save(commit = True)
        return HttpResponseRedirect('/')

def add_assets(request):
    assets = Asset.objects.all()    
    if request.method == 'POST':
        form = AssetForm(request.POST,request.FILES)
        if form.is_valid():
            asset = Asset(name = form.cleaned_data['name'],location = form.cleaned_data['location'],room = form.cleaned_data['room'])
            for i in assets:
                if i.name == asset.name:
                    my_record = AssetForm(request.POST, instance=i)
                    my_record.save()
                    return HttpResponseRedirect('/')
            asset.save()
            return HttpResponseRedirect('/')
    else:
        form = AssetForm()
        return render(request, 'DjangoAssetManagement/index.html', {'form': form})

def all_assets(request):
    name = "List of All Assets"
    lastRoom = 0
    aList = []
    bList= []
    assets = Asset.objects.all()
    buildings = Building.objects.all()
    for building in buildings:
        bList.append(building)
        for f in building.Asset.all():
            aList.append(f)
        aList.sort(key=lambda x: (x.location.name,x.room), reverse=True)
    moves = len(assets)
    return render(request, 'DjangoAssetManagement/all-assets.html', {'name':name,'assets':aList,'buildings':bList,'moves':moves})
    
def building_list(request, buildingI):
    name = buildingI
    buildings = Building.objects.get(name=buildingI)
    listo=[]
    for f in buildings.Asset.all():
        listo.append(f)
    listo.sort(key=lambda x: x.room, reverse=True)
    num_of_assets = len(listo)
    return render(request, 'DjangoAssetManagement/building_list.html', {'name':name,'building':name,'assets':listo,'num_of_assets':num_of_assets})


def search_form(request):
    name = "Search Form"
    return render(request, 'DjangoAssetManagement/search_form.html', {'name':name})


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        assets = Asset.objects.filter(name__icontains=q)
        return render(request, 'DjangoAssetManagement/search_results.html',
                      {'assets': assets, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')


def export_moves(request):
    lastLoc = ""
    lastRoom = ""
    listo=[]
    assets = Asset.objects.all()
    buildings = Building.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asset-list.csv"'
    
    writer = csv.writer(response)
    for building in buildings:
        for f in building.Asset.all():
            listo.append(f)
        listo.sort(key=lambda x: (x.location.name,x.room), reverse=True)
    
    for x in listo:
        if lastLoc != x.location:
            lastRoom = x.location
            writer.writerow([""])
            writer.writerow([x.location])
        if lastRoom != x.room:
            lastRoom = x.room
            writer.writerow(["",x.room])
        writer.writerow([x.name, x.room, x.pub_date])

    return response
