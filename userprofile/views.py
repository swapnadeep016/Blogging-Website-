from django.shortcuts import render, redirect
from .models import User_profileing
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from binascii import a2b_base64

import face_recognition

# Machinelearning packages & libraries

import base64
from PIL import Image
import numpy as np
import io
import cv2
import ast



def home(request):
	return render(request, 'index.html')

def signup_call(request):
	if request.method=='POST':
		email=request.POST['email']
		uname=request.POST['username']
		passwd=request.POST['password']
		
		img=request.POST['userimage']
		
		#print(img)
		i = base64.b64decode(img[22:])
		image = Image.open(io.BytesIO(i))
		imarr = np.array(image)                                                                                                                                                                                                                                                    
		#print(imarr)
		locations = face_recognition.face_locations(imarr, model="cnn")
		#print(locations)

		encodings = face_recognition.face_encodings(imarr, locations)

		url = ''
		
		if(len(encodings) == 0 ) :
				return HttpResponse('<script>alert("Face is not capured properly");window.location="%s"</script>'%url)
		if(len(encodings)>1) :
			  return HttpResponse('<script>alert("Too many Faces catured");window.location="%s"</script>'%url)
		if(len(encodings)==1) :
			  emb1  = list(encodings[0])
			  emb = str(emb1)
			  #print(emb)
		a = User_profileing.objects.all().values('username', 'embeddings',"image64")
		


		usernames = []
		embeddings = []
		for x in a :
			#print(x["username"])
			usernames.append(x["username"])
			#print(x["embeddings"])
			#print("@@@@@@@@@@@@")
			#print(type(x["embeddings"]))
			embedarray = ast.literal_eval(x["embeddings"])
			#print(type(embedarray))
			#print(embedarray)
			embeddings.append(embedarray)

		results = face_recognition.compare_faces(np.array(embeddings), np.array(emb1),0.4)
		url=''
		if(results.count("True")==1) :
			return HttpResponse('<script>alert("Alrready have one account with the Same Face");window.location="%s"</script>'%url)

			  


		#print(imarr)

		
		try:

			u=User_profileing(email=email,username=uname,password=passwd,embeddings = emb,image64=img)
			u.save()
			newuser =User(email=email,username=uname, password=make_password(passwd))
			newuser.save()
			
			return redirect('/user/login/')
		except:
			return HttpResponse('<script>alert("Username already exists..");window.location="%s"</script>'%url)
		return redirect('/user/signup/')
		
	return render(request,'signup.html')




	
def logout_call(request):
	logout(request)
	return redirect('/user/login/')


def facelogin(request) :
	url = ''
	if request.method=='POST':
		
		img=request.POST['face_login_image']

		if img=='':
			return HttpResponse('<script>alert("Capture Image First");window.location="%s"</script>'%url)
		
		i = base64.b64decode(img[22:])
		image = Image.open(io.BytesIO(i))
		imarr = np.array(image)

		#print(imarr)
		locations = face_recognition.face_locations(imarr, model="cnn")
		#print(locations)

		encodings = face_recognition.face_encodings(imarr, locations)

		
		
		if(len(encodings) == 0 ) :
				return HttpResponse('<script>alert("Face is not capured properly");window.location="%s"</script>'%url)
		if(len(encodings)>1) :
			  return HttpResponse('<script>alert("Too many Faces catured");window.location="%s"</script>'%url)
		if(len(encodings)==1) :
			  emb  = list(encodings[0])
		a = User_profileing.objects.all().values('username', 'embeddings',"image64")
		import ast


		usernames = []
		embeddings = []
		for x in a :
			#print(x["username"])
			usernames.append(x["username"])
			#print(x["embeddings"])
			#print("@@@@@@@@@@@@")
			#print(type(x["embeddings"]))
			embedarray = ast.literal_eval(x["embeddings"])
			#print(type(embedarray))
			#print(embedarray)
			embeddings.append(embedarray)

		results = face_recognition.compare_faces(np.array(embeddings), np.array(emb),0.4)
		url=''
		print(results)
		if (results.count(True) == 0) :
			return HttpResponse('<script>alert("You have not registerd yet create an account ");window.location="%s"</script>'%url)
		if (results.count(True) >= 2) :
			return HttpResponse('<script>alert("FACE IS NOT CAPTURED PROPERLY FIT YOUR FACE INTO THE RECTANGULAR BOX ");window.location="%s"</script>'%url)
		match = usernames[results.index(True)]

		passwd=request.POST['password']
		
		try:
			selUser = authenticate(username=match, password=passwd)

			#print(selUser)
			if selUser:
				#print('came')
				login(request,selUser)
				#print(5)
				return redirect('/blog/dashboard')
		except:
			return HttpResponse('<script>alert("wrong password or username");window.location="%s"</script>'%url)


	return render(request, 'login.html')

			