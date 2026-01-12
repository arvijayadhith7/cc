from django.shortcuts import render
from django.apps import apps
from . import models


# Create your views here.


def rights(request):
    model = apps.get_model('right', 'RightTableList')
    data = model.objects.values('name', 'description','tname').distinct()
    return render(request, "rights.html", {'data': data})

def article(request, tn):
    model = apps.get_model('right',tn)
    data = model.objects.values() 
    mod = apps.get_model('right','Righttablelist')
    act = mod.objects.filter(tname=tn)
    return render(request, "article.html", {'data': data, 'tn':tn, 'act':act})

def right_detail(request, tn, no):
    model = apps.get_model('right', tn)
    data = model.objects.filter(section=no)
    
    # Navigation logic
    prev_section = model.objects.filter(section=no-1).first() if no > 1 else None
    next_section = model.objects.filter(section=no+1).first()

    return render(request, "rightdetails.html", {
        'data': data, 
        'tname': tn,
        'prev_section': prev_section,
        'next_section': next_section
    })