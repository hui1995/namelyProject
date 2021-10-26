from django.test import TestCase

# Create your tests here.
import uuid
import requests
response=requests.get("https://img3.doubanio.com/view/subject/s/public/s1067911.jpg")
name=str(uuid.uuid4())+".jpg"
with open(name,"wb") as f:
    f.write(response.content)
