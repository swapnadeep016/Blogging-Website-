from django.shortcuts import render,redirect
from .models import publishedblog,draftblog
from userprofile.models import User_profileing
from django.http import HttpResponse

import base64
from PIL import Image
from io import BytesIO

from operator import itemgetter
import numpy as np
import ast
from scipy import spatial

import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import numpy as np


def read_article(t):
	article = t.split(". ")
	print(len(article))
	sentences = []

	for sentence in article:
		print(sentence)
		print()
		sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))


	return sentences


word_embeddings = {}
f = open('blog\summarizer\glove.6B.50d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()


def word_embedd_sentence_similarity(sent1, sent2, word_embeddings, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1 if w not in stopwords]
    sent2 = [w.lower() for w in sent2 if w not in stopwords]



    # build the vector for the first sentence
    if len(sent1) != 0:

        vector1 = sum([word_embeddings.get(w, np.zeros((50,))) for w in sent1 ])/(len(sent1)+0.001)
    else:
        vector1 = np.zeros((50,))

    if len(sent2) != 0:

        vector2 = sum([word_embeddings.get(w, np.zeros((50,))) for w in sent2 ])/(len(sent2)+0.001)
    else:
        vector2 = np.zeros((50,))

    # build the vector for the second sentence
    print(vector1,vector2)

    return 1 - cosine_distance(vector1, vector2)


def embed_build_similarity_matrix(sentences,word_embeddings, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = word_embedd_sentence_similarity(sentences[idx1], sentences[idx2], word_embeddings,stop_words)

    return similarity_matrix

nltk.download("stopwords")


# Create your views here.
def home(request):
	#print(1)
	u=request.user.username
	usr=User_profileing.objects.get(username=request.user)
	#print(usr)
	img=usr.image64
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
	return render(request,'dashboard.html',{'name':u,'image':img,'nb1':nb1,'nb2':nb2,'nb3':nb3})


def addblog(request):
	uno=request.user.username
	uid=request.user.id
	url=''
	if request.method=='POST':
		ndr=request.POST['submit']
		ntitle=request.POST['title']
		nsummary=request.POST['summary']
		ncontent=request.POST['content']

		nbyuser=request.POST['user']
		print(nbyuser)

		nimage1=request.FILES['blogimage1']
		nimage2=request.FILES['blogimage2']
		nimage3=request.FILES['blogimage3']

		ntag=request.POST['tag']
		#imgfile=request.FILES.getlist('image')
		#print(imgfile)
		#print(ndraft)
		stop_words = stopwords.words('english')
		l= ncontent.split(". ")
		t = ncontent
		sentences =  read_article(t)
		global word_embeddings
		ai_generated_summary = ncontent
		if len(sentences) <= 6 :
			ai_generated_summary = ncontent

		else :
			sentence_similarity_martix =  embed_build_similarity_matrix(sentences, word_embeddings,stop_words)
			sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
			scores = nx.pagerank(sentence_similarity_graph)
			ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(l)), reverse=True)
			k = len(sentences)//2
			summarize_text=""
			for i in range(3):
				summarize_text = summarize_text + str(ranked_sentence[i][1]) + " "

			ai_generated_summary = summarize_text

		usr=User_profileing.objects.get(username = nbyuser)
		if ndr=='Draft':
			n=draftblog(dtitle=ntitle,dsummary=nsummary,dcontent=ncontent,dai_generated_summary = ai_generated_summary,dimage1=nimage1,dimage2=nimage2,dimage3=nimage3,dbyuser=usr,dtags=ntag)
			n.save()
			return HttpResponse('<script>alert("Blog Saved in Draft");window.location="%s"</script>'%url)
		elif ndr=='Publish':
			#print(sentence_vector)

			m=publishedblog(title=ntitle,summary=nsummary,content=ncontent,ai_generated_summary = ai_generated_summary,image1=nimage1,image2=nimage2,image3=nimage3,byuser=usr,tags=ntag)
			m.save()

			return HttpResponse('<script>alert("Blog Saved");window.location="%s"</script>'%url)

	return render(request,'addblog.html',{'name':uno,'id':uid})



def draft(request):
	u=User_profileing.objects.get(username=request.user)
	n=draftblog.objects.filter(dbyuser=u)
	#print(n)
	return render(request,'draft.html',{'name':u.username,'db':n})

def published(request):
	u=User_profileing.objects.get(username=request.user)
	p=publishedblog.objects.filter(byuser=u)
	return render(request,'published.html',{'name':u.username,'pb':p})



def showblog(request,id):
	#u=User_profileing.objects.get(username=request.user)
	name=request.user
	try:
		uobj=User_profileing.objects.get(username=request.user.username)
		u=uobj.username
	except:
		u=""
	#print("hey",name)
	if name=="AnonymousUser":
		#print(1)
		nam1=" "
	else:
		nam1=request.user

	print(name)
	p=publishedblog.objects.get(id=id)
	return render(request,'showblog.html',{'blog':p,'name':nam1,'user':u})

def drafttopub(request,id):
	url=""
	try:
		d=draftblog.objects.get(id=id)
		#print(d.dimage2,d.dimage3)
		#u=User_profileing.objects.get(username=d.dbyuser)

		p=publishedblog(title=d.dtitle,summary=d.dsummary,content=d.dcontent,image1=d.dimage1,image2=d.dimage2,image3=d.dimage3,byuser=d.dbyuser)
		#print(p)
		p.save()
		#print('here')
		d2=draftblog.objects.filter(id=id)
		d2.delete()

		return HttpResponse('<script>alert("Blog Published");window.location="%s"</script>'%url)

	except:
		return redirect('/blog/draft')

	return redirect('/blog/draft')


def drafttodel(request,id):
	d=draftblog.objects.filter(id=id)
	d.delete()
	return redirect('/blog/draft')

def publishtodel(request,id):
	p=publishedblog.objects.filter(id=id)
	p.delete()
	return redirect('/blog/published')

def allblog(request):
	p=publishedblog.objects.all()
	return render(request,'allblog.html',{'blog':p,'name':request.user})
