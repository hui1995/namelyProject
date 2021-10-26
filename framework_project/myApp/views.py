from django.shortcuts import render,HttpResponse
from django.template import loader
from django.views import View

# Create your views here.

class LoginView(View):
    def get(self,request):
        return render(request,'login.html',locals())

def index(request):
    context = {}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    print(load_template)
    template = loader.get_template('' + load_template)
    return HttpResponse(template.render(context, request))
