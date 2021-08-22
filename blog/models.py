from django.db import models
from userprofile.models import User_profileing
from django.contrib.auth.models import User

# Create your models here.
class publishedblog(models.Model):
	title =models.CharField(max_length= 500)
	summary=models.CharField(max_length=3000)
	content = models.TextField()
	ai_generated_summary = models.TextField()
	image1= models.ImageField(upload_to='media/pblog')
	image2= models.ImageField(upload_to='media/pblog')
	image3= models.ImageField(upload_to='media/pblog')
	byuser= models.ForeignKey(User_profileing, on_delete=models.DO_NOTHING)
	tags=models.CharField(max_length=3000)
	date=models.DateTimeField(auto_now_add=True)



	def __str__(self):
		return self.title

class draftblog(models.Model):
	dtitle =models.CharField(max_length= 500)
	dsummary=models.CharField(max_length=3000)
	dcontent = models.TextField()
	dai_generated_summary = models.TextField()
	dimage1= models.ImageField(upload_to='media/dblog')
	dimage2= models.ImageField(upload_to='media/dblog')
	dimage3= models.ImageField(upload_to='media/dblog')
	dtags=models.CharField(max_length=3000)
	dbyuser= models.ForeignKey(User_profileing, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.dtitle

class bookmarked(models.Model):
	bbyuser=models.ForeignKey(User,on_delete=models.DO_NOTHING)
	blog=models.ForeignKey(publishedblog,on_delete=models.DO_NOTHING)
