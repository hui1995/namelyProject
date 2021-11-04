from django.shortcuts import render,redirect
from django.views import View
#!/usr/bin/env python
# -*- encoding: utf-8 -*-



# Create your views here.

class HomeView(View):
    def get(self,request):
        return render(request,'home.html')

    def post(self,request):
        
        return redirect("")
class InformationView(View):
    def get(self,request):
        return render(request,'information.html')

class MemebersView(View):
    def get(self,request):
        return render(request,'memeber.html')


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

class MessageView(View):
    def get(self,request):
        return render(request,'message.html')