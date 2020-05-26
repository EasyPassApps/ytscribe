from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from youtube_transcript_api import YouTubeTranscriptApi
from punctuator import Punctuator
import os
from django.conf import settings
# from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import RedirectView
from django.shortcuts import redirect
from youtube_scraper.scraper import scrape_url
import time
import re

def test(request):
	video_id = "5v1B1R3lEO8"
	srt = YouTubeTranscriptApi.get_transcript(video_id)
	alltext = ""
	for item in srt:
		alltext = alltext + item['text']+" "
	print(os.path.join(settings.BASE_DIR))
	file_ = os.path.join(settings.BASE_DIR, 'model.pcl')
	p = Punctuator(file_)
	punctuated = p.punctuate(alltext[:5000])
	specialtag = punctuated.split('.')
	# newpara = ""
	# for item in specialtag:
	# 	newpara = newpara + item+".<br>"

	#specialtag = alltext


	return render(request, 'test.html', {
        'foo': specialtag,
    })

# def new_post(request):
# 	form = PostForm(request.POST or None)
# 	section = form.save(commit=False)
# 	print(section.title)
# 	section.body = "WOOO IM OVERWRITING YOU BITCH"
# 	section.save()
# 	if form.is_valid():
# 		form.save()
# 	else:
# 		form = PostForm()
# 	context = {
# 	'form':form,
# 	}
# 	print(form.model)
# 	#print(Post.get_absolute_url(request.id))


# 	return render(request,'new_post.html',context)

def get_sec(time_str):
	h, m, s = time_str.split(':')
	return int(h) * 3600 + int(m) * 60 + int(s)

class HomeView(ListView):
	model = Post
	template_name = 'home.html'


class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

class AddPostView(CreateView):
	model = Post
	template_name = 'add_post.html'
	fields ='__all__'
	yo = "FIbvt4_InyU"

	
		
	def form_valid(self, form):
		self.object = form.save(commit=False)
		video_id = self.object.body.split('?v=')[1].split("&")[0]
		self.object.vid_id = video_id
		print('Does he have it?')
		print(self.object.vid_id)
		if(Post.objects.filter(vid_id=self.object.vid_id).exists()):
			yo = Post.objects.filter(vid_id=self.object.vid_id)[:1]
			print(yo[0].pk)
			print('REDIRECT!')
			return HttpResponseRedirect(reverse('article-detail', kwargs={'pk': str(yo[0].pk),"yt":video_id}))
			#return redirect('article-detail', post.pk post.vid_id+str(yo[0].pk)+'/'+str(video_id))
		
		data = scrape_url('http://youtube.com/watch?v='+video_id)
		print(data.title)
		print(data.poster)
		srt = YouTubeTranscriptApi.get_transcript(video_id)
		totalduration = 0
		alltext = ""
		for item in srt:
			go = item['start']
			if(go - totalduration > 30):
				alltext = alltext + time.strftime('%H:%M:%S', time.gmtime(item['start']))+ item['text']+" "
				totalduration = item['start']
			else:
				alltext = alltext + item['text']+" "
		
		r = re.findall('(?:[0123456789]\d|2[0123456789]):(?:[0123456789]\d):(?:[0123456789]\d)', alltext)
		for item in r:
			# print(item)
			alltext =  alltext.replace(item,"<br><a class='ytlink' href='#' type='button' onclick='seek("+str(get_sec(item))+")'>"+item+"</a> </br>")

		print(alltext)
		file_ = os.path.join(settings.BASE_DIR, 'model.pcl')
		p = Punctuator(file_)
		punctuated = p.punctuate(alltext)
		
		self.object.title = data.title
		self.object.title_tag = data.poster
		# totaltext = punctuated.split(".")
		# finaltext = ""
		# for item in totaltext:
		# 	finaltext = finaltext + item +"."+"<br><br>"
		iframe = '''<iframe id="player" type="text/html" width="560" height="315" src="http://www.youtube.com/embed/PjDw3azfZWI?enablejsapi=1" frameborder="0"></iframe>'''
		embed = '''<iframe id="player" type="text/html" width="560" height="315" src="http://www.youtube.com/embed/'''+video_id+'''?enablejsapi=1" frameborder="0"></iframe>'''
		self.object.body = embed+"<br>"+alltext
		
			

		self.object.save()
		return HttpResponseRedirect(reverse('article-detail', kwargs={'pk': self.object.id,"yt":video_id}))
		#return http.HttpResponseRedirect(self.get_success_url())
		#return super().form_valid(form)



class Test(ListView):
	model = Post
	template_name = 'test.html'
	fields ='__all__'
