from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from youtube_transcript_api import YouTubeTranscriptApi
import requests

class Post(models.Model):
	title = models.CharField(max_length=255, default="New Post")
	title_tag = models.CharField(max_length=255, default="Blog Post")
	auth = models.ForeignKey(User, on_delete=models.CASCADE,default="cny")
	body = models.CharField(max_length=255)
	#youtube_video = models.CharField(max_length=255)
	vid_id= models.CharField(max_length=255, default="5v1B1R3lEO8")
	video_id = "5v1B1R3lEO8"
	srt = YouTubeTranscriptApi.get_transcript(video_id)
	alltext = ""
	for item in srt:
		if len(item) > 4:
			alltext = alltext + item['text']+" "
	# print('text is ready')
	# url = "http://bark.phon.ioc.ee/punctuator"
	# data = {"text": alltext}
	# par = requests.post(url, data).text
	specialtag = alltext

	def __str__(self):
		return self.title + ' | ' + str(self.auth)

	def get_absolute_url(self):
		return reverse('article-detail', kwargs={'pk': self.pk,"yt":self.video_id})

