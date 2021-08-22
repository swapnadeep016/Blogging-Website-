from django.shortcuts import render,redirect
from blog.models import publishedblog
from userprofile.models import User_profileing
import random


def home(request):
	try:
		pb=publishedblog.objects.all().last()
		#print(pb)
		nnb1= publishedblog.objects.all()
		count=nnb1.count()
		#print(count)
		no1=count-1
		no2=count-2
		no3=count-3
		nb1=nnb1[no1]
		#print(nb1)
		nb2=nnb1[no2]
		#print(nb2)
		nb3=nnb1[no3]
		#print(nb3)
	except:
		return render(request,'error.html')

	try:
		uobj=User_profileing.objects.get(username=request.user.username)
		u=uobj.username
	except:
		u=""
		
	return render(request,'index.html',{'lblog':pb,'nb1':nb1,'nb2':nb2,'nb3':nb3,'user':u})