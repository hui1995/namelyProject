from django.shortcuts import render,HttpResponse
from django.template import loader
from django.views import View
import csv
from .models import GameModel,EventModel,Medals
# Create your views here.

class LoginView(View):
    def get(self,request):
   

        return render(request,'login.html',locals())

def index(request):

    with open("a.csv",encoding="utf8") as f:
        reader=csv.reader(f)
        header_row=next(reader)
        int1 =1;
        for i in reader:
            try:
                event=EventModel.objects.filter(event=i[4],gender=i[9]).first()
                game=GameModel.objects.filter(sport=i[2],discipline=i[3]).first() 
                Medals.objects.create(city=i[0],year=i[1],gid=game,eid=event,athlete=i[5],gender=i[6],country_code=i[7],country=i[8],medal=i[10])
            except:
                continue    


        return HttpResponse("ok")


    # return HttpResponse(template.render(context, request))

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    print(load_template)
    template = loader.get_template('' + load_template)
    return HttpResponse(template.render(context, request))
