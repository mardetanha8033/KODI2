# -*- coding: utf-8 -*-
from LIBRARY import *

#website0a = 'https://vod.alarab.com/view-1/افلام-عربية'
#website0a = 'http://tv.alarab.com'
#website0a = 'http://tv1.alarab.com'
#website0a = 'http://vod.alarab.com/index.php'

script_name = 'ALARAB'
headers = {'User-Agent':''}
menu_name='_KLA_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==10: results = MENU(url)
	elif mode==11: results = TITLES(url)
	elif mode==12: results = PLAY(url)
	elif mode==13: results = EPISODES(url)
	elif mode==14: results = LATEST()
	elif mode==15: results = RAMADAN_MENU()
	elif mode==16: results = RAMADAN()
	elif mode==19: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	addMenuItem('folder',menu_name+'بحث في الموقع','',19,'','','_REMEMBERRESULTS_')
	addMenuItem('folder',website+'___'+menu_name+'اخر الاضافات','',14)
	addMenuItem('folder',website+'___'+menu_name+'مسلسلات رمضان','',15)
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,'','ALARAB-MENU-1st')
	html_blocks=re.findall('id="nav-slider"(.*?)</div>',html,re.DOTALL)
	block1 = html_blocks[0]
	items = re.findall('href="(.*?)".*?>(.*?)<',block1,re.DOTALL)
	for link,title in items:
		link = website0a+link
		title = title.strip(' ')
		addMenuItem('folder',website+'___'+menu_name+title,link,11)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('id="navbar"(.*?)</div>',html,re.DOTALL)
	block2 = html_blocks[0]
	items = re.findall('href="(.*?)".*?>(.*?)<',block2,re.DOTALL)
	for link,title in items:
		link = website0a+link
		addMenuItem('folder',website+'___'+menu_name+title,link,11)
	return html

def RAMADAN_MENU():
	#addMenuItem('folder',menu_name+'المسلسلات العربية',website0a+'/view-8/مسلسلات-عربية',11)
	addMenuItem('folder',menu_name+'مسلسلات رمضان 2020 ؟!','',16)
	addMenuItem('folder',menu_name+'مسلسلات رمضان 2020',website0a+'/view-8/مسلسلات-رمضان-2020',11)
	addMenuItem('folder',menu_name+'مسلسلات رمضان 2019',website0a+'/ramadan2019/مصرية',11)
	addMenuItem('folder',menu_name+'مسلسلات رمضان 2018',website0a+'/ramadan2018/مصرية',11)
	addMenuItem('folder',menu_name+'مسلسلات رمضان 2017',website0a+'/ramadan2017/مصرية',11)
	addMenuItem('folder',menu_name+'مسلسلات رمضان 2016',website0a+'/ramadan2016/مصرية',11)
	return

def LATEST():
	html = OPENURL_CACHED(REGULAR_CACHE,website0a,'',headers,True,'ALARAB-LATEST-1st')
	#DIALOG_OK('',html)
	html_blocks=re.findall('heading-top(.*?)div class=',html,re.DOTALL)
	block = html_blocks[0]+html_blocks[1]
	items=re.findall('href="(.*?)".*?data-src="(.*?)" alt="(.*?)"',block,re.DOTALL)
	for link,img,title in items:
		url = website0a + link
		if 'series' in url: addMenuItem('folder',menu_name+title,url,11,img)
		else: addMenuItem('video',menu_name+title,url,12,img)
	return

def TITLES(url):
	#DIALOG_OK('TITLES',url)
	response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'',headers,True,True,'ALARAB-TITLES-1st')
	html = response.content
	#with open('S:\\00emad.html','w') as f: f.write(str(html))
	html_blocks = re.findall('video-category(.*?)right_content',html,re.DOTALL)
	if not html_blocks: return
	block = html_blocks[0]
	found = False
	#items = re.findall('src="(http.*?)".*?<h[52].*?href="(.*?)">(.*?)<',block,re.DOTALL)
	items = re.findall('video-box.*?href="(.*?)".*?src="(http.*?)" alt="(.*?)"',block,re.DOTALL)
	allTitles,itemsNEW = [],[]
	for link,img,title in items:
		if title=='': title = link.split('/')[-1].replace('-',' ')
		sequence = re.findall('(\d+)',title,re.DOTALL)
		if sequence: sequence = int(sequence[0])
		else: sequence = ''
		itemsNEW.append([img,link,title,sequence])
	itemsNEW = sorted(itemsNEW, reverse=True, key=lambda key: key[3])
	#DIALOG_OK('222',url)
	for img,link,title,sequence in itemsNEW:
		link = website0a + link
		#DIALOG_OK(url,title)
		title = title.replace('مشاهدة مسلسل','مسلسل')
		title = title.replace('مشاهدة المسلسل','المسلسل')
		title = title.replace('مشاهدة فيلم','فيلم')
		title = title.replace('مشاهدة الفيلم','الفيلم')
		title = title.replace('مباشرة كواليتي','')
		title = title.replace('عالية على العرب','')
		title = title.replace('مشاهدة مباشرة','')
		title = title.replace('اون لاين','')
		title = title.replace('اونلاين','')
		title = title.replace('بجودة عالية','')
		title = title.replace('جودة عالية','')
		title = title.replace('بدون تحميل','')
		title = title.replace('على العرب','')
		title = title.replace('مباشرة','')
		title = title.strip(' ').replace('  ',' ').replace('  ',' ')
		title = '_MOD_'+title
		title2 = title
		if '/q/' in url and ('الحلقة' in title or 'الحلقه' in title):
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode: title2 = episode[0]
			#if 'مسلسل' not in title2: title2 = 'مسلسل '+title2
		if title2 not in allTitles:
			allTitles.append(title2)
			#xbmc.log(title2, level=xbmc.LOGNOTICE)
			if '/q/' in url and ('الحلقة' in title or 'الحلقه' in title):
				addMenuItem('folder',menu_name+title2,link,13,img)
				found = True
			elif 'series' in link:
				addMenuItem('folder',menu_name+title,link,11,img)
				found = True
			else:
				#if 'مسلسل' not in title and 'الحلقة' in title: title = 'مسلسل '+title
				addMenuItem('video',menu_name+title,link,12,img)
				found = True
	#DIALOG_OK('333',url)
	if found:
		items = re.findall('tsc_3d_button red.*?href="(.*?)" title="(.*?)"',block,re.DOTALL)
		for link,page in items:
			url = website0a + link
			addMenuItem('folder',menu_name+page,url,11)
	return

def EPISODES(url):
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'ALARAB-EPISODES-1st')
	series = re.findall('href="(/series.*?)"',html,re.DOTALL)
	url2 = website0a+series[0]
	results = TITLES(url2)
	return

"""
def EPISODES_OLD(url):
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'ALARAB-EPISODES_OLD-1st')
	html_blocks = re.findall('banner-right(.*?)classic-channel',html,re.DOTALL)
	#DIALOG_OK(url,'step 2')
	block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	#DIALOG_OK(url,'step 3')
	items = sorted(items, reverse=True, key=lambda key: key[1])
	#name = xbmc.getInfoLabel('ListItem.Label')
	#DIALOG_OK(url,'step 4')
	allTitles = []
	for img,link,title in items:
		if title not in allTitles:
			link = website0a+unquote(link)
			title = title.strip(' ')
			addMenuItem('video',menu_name+'مسلسل '+title,link,12,img)
			allTitles.append(title)
	#DIALOG_OK(url,'step 5')
	return
"""

def PLAY(url):
	#DIALOG_OK(url,str(url))
	linkLIST,titleLIST,videodeliveryID = [],[],[]
	html = OPENURL_CACHED(SHORT_CACHE,url,'',headers,True,'ALARAB-PLAY-1st')
	if 'vid=' in html:
		# https://vod.alarab.com/v101949-_حلقة_25_حكايتي_HD_رمضان_252019
		url2 = re.findall('class="resp.*?src="(.*?)"',html,re.DOTALL)
		if url2:
			url2 = url2[0]
			html2 = OPENURL_CACHED(LONG_CACHE,url2,'',headers,True,'ALARAB-PLAY-2nd')
			url3 = re.findall('source src="(.*?)"',html2,re.DOTALL)
			if url3:
				url3 = url3[0]
				#if url3.count('http')>1: url3 = 'http'+url3.split('http',2)[2]
				linkLIST.append(url3)
				titleLIST.append('سيرفر خاص  m3u8')
	else:
		if '/viewVedio/' in url:
			id = re.findall('.com/viewVedio/([0-9]+)/',url,re.DOTALL)
		else:
			id = re.findall('.com/v([0-9]+)-',url,re.DOTALL)
		if id:
			url2 = 'https://alarabplayers.alarab.com/vod.php?vid='+id
			headers['Referer'] = url
			html2 = OPENURL_CACHED(SHORT_CACHE,url2,'',headers,True,'ALARAB-PLAY-3rd')
			html += html2
		html_blocks = re.findall('playerInstance.setup(.*?)primary',html,re.DOTALL)
		for block in html_blocks:
			youtube = re.findall('file:".*?youtu.*?=(.*?)"',block,re.DOTALL)
			items1 = re.findall('file: ["\'](.*?mp4)["\'].*?label: "(.*?)"',block,re.DOTALL)
			items2 = re.findall('file: ["\'].*?videodelivery.*?/(.*?)/',block,re.DOTALL)
			items3 = re.findall('file: ["\'](.*?)["\']',block,re.DOTALL)
			items4 = re.findall('"file": ["\'](.*?)["\']',block,re.DOTALL)
			if youtube:
				for youtubeID in youtube:
					#url = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
					linkLIST.append(youtubeID)
					titleLIST.append('ملف يوتيوب')
			elif items1:
				for file,label in reversed(items1):
					linkLIST.append(file)
					titleLIST.append('سيرفر خاص  mp4  '+label)
			elif items2:
				for id in items2:
					videodeliveryID.append(id)
			elif items3:
				for file in items3:
					linkLIST.append(file)
					titleLIST.append('سيرفر خاص  mp4')
			elif items4:
				# https://cdn.alarab.com/vod,6,15,00/130479.mp4.urlset/playlist.m3u8
				for file in items4:
					titleLIST2,linkLIST2 = EXTRACT_M3U8(file)
					z = zip(titleLIST2,linkLIST2)
					for label,file in z:
						linkLIST.append(file)
						titleLIST.append('سيرفر خاص  '+label)
		id = re.findall('stream src="(.*?)"',html,re.DOTALL)
		if id: videodeliveryID.append(id)
		for id in videodeliveryID:
			url3 = 'https://videodelivery.net/'+id+'/manifest/video.mpd'
			linkLIST.append(url3)
			titleLIST.append('سيرفر خاص  mpd')
			url3 = 'https://videodelivery.net/'+id+'/manifest/video.m3u8'
			title = 'سيرفر خاص  m3u8'
			titleLIST.append(title)
			linkLIST.append(url3)
		"""
		html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'ALARAB-PLAY-3rd')
		DIALOG_OK(url,str(html))
		items2 = re.findall('RESOLUTION=(.*?),.*?\n(.*?)\n',html,re.DOTALL)
		if items2:
			for resolution,link in items2:
				title = ' سيرفر خاص '+'m3u8 '+resolution.split('x')[1]
				link = 'https://videodelivery.net/'+videodeliveryID[0]+'/manifest/'+link
				titleLIST.append(title)
				linkLIST.append(link)
		#items = re.findall('resp-container.*?src="(.*?)".*?</div>',html,re.DOTALL)
		#if items:
		#	url = items[0]
		#	linkLIST.append(url)
		#	titleLIST.append('ملف التشغيل')
		#DIALOG_OK('',str(linkLIST))
		#url = website0a + '/download.php?file='+id
		#html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'ALARAB-PLAY-4th')
		#items = re.findall('</h2>.*?href="(.*?mp4)"',html,re.DOTALL)
		#if items:
		#	linkLIST.append(items[0])
		#	titleLIST.append('ملف التحميل')
		"""
	if len(linkLIST)==0:
		LOG_THIS('NOTICE',LOGGING(script_name)+'   No video file found   URL: [ '+url+' ]')
		DIALOG_OK('رسالة من المبرمج','لا يوجد ملف فيديو')
		return
	elif len(linkLIST)==1:
		selection = 0
		url = linkLIST[selection]
	else:
		new_linkLIST,new_titleLIST = [],[]
		for i in range(0,len(linkLIST),+1):
			if linkLIST[i] not in new_linkLIST:
				new_linkLIST.append(linkLIST[i])
				new_titleLIST.append(titleLIST[i])
		selection = DIALOG_SELECT('اختر الملف المناسب:', new_titleLIST)
		if selection == -1 : return
		url = new_linkLIST[selection]
	if 'youtu' in url:
		#DIALOG_OK(url,'')
		import RESOLVERS
		RESOLVERS.PLAY_LINK(url,script_name,'video')
	else: PLAY_VIDEO(url,script_name,'video')
	return

def RAMADAN():
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,True,'ALARAB-RAMADAN-1st')
	html_blocks=re.findall('id="content_sec"(.*?)id="left_content"',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	year = re.findall('/ramadan([0-9]+)/',str(items),re.DOTALL)
	year = year[0]
	for link,title in items:
		url = website0a + link
		title = title.strip(' ') + ' ' + year
		addMenuItem('folder',menu_name+title,url,11)
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','%20')
	url = website0a + "/q/" + new_search
	#DIALOG_OK('333',url)
	results = TITLES(url)
	return



