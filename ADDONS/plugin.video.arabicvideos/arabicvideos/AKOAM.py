# -*- coding: utf-8 -*-
from LIBRARY import *

headers = { 'User-Agent' : '' }
script_name='AKOAM'
menu_name='_AKO_'
website0a = WEBSITES[script_name][0]
noEpisodesLIST = ['فيلم','كليب','العرض الاسبوعي','مسرحية','مسرحيه','اغنية','اعلان','لقاء']

def MAIN(mode,url,text):
	#XBMCGUI_DIALOG_OK(text,str(mode))
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==70: results = MENU(url)
	elif mode==71: results = CATEGORIES(url)
	elif mode==72: results = TITLES(url,text)
	elif mode==73: results = SECTIONS(url)
	elif mode==74: results = PLAY(url)
	elif mode==79: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	addMenuItem('folder',menu_name+'بحث في الموقع','',79,'','','_REMEMBERRESULTS_')
	addMenuItem('folder',menu_name+'سلسلة افلام','',79,'','','سلسلة افلام')
	addMenuItem('folder',menu_name+'سلاسل منوعة','',79,'','','سلسلة')
	#addMenuItem('folder',website+'___'+menu_name+'المميزة',website0a,72,'','','featured')
	#addMenuItem('folder',website+'___'+menu_name+'المزيد',website0a,72,'','','more')
	#addMenuItem('folder',website+'___'+menu_name+'الأخبار',website0a,72,'','','news')
	#addMenuItem('folder',website+'___'+menu_name+'الأخبار',website0a,72,'','','news')
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	ignoreLIST = ['الكتب و الابحاث','الكورسات التعليمية','الألعاب','البرامج','الاجهزة اللوحية','الصور و الخلفيات','المصارعة الحرة']
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','AKOAM-MENU-1st')
	html_blocks = re.findall('big_parts_menu(.*?)class="sidebar_search',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title not in ignoreLIST:
				addMenuItem('folder',website+'___'+menu_name+title,link,71)
	addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	return html

def CATEGORIES(url):
	html = openURL_cached(LONG_CACHE,url,'',headers,'','AKOAM-CATEGORIES-1st')
	html_blocks = re.findall('sect_parts(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = title.strip(' ')
			addMenuItem('folder',menu_name+title,link,72)
		addMenuItem('folder',menu_name+'جميع الفروع',url,72)
	else: TITLES(url,'')
	return

def TITLES(url,type):
	#XBMCGUI_DIALOG_OK(url,type)
	html = openURL_cached(REGULAR_CACHE,url,'',headers,True,'AKOAM-TITLES-1st')
	items = []
	if type=='featured':
		html_blocks = re.findall('section_title featured_title(.*?)subjects-crousel',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)"><div class="subject_box.*?src="(.*?)".*?<h3.*?>(.*?)</h3>',block,re.DOTALL)
	elif type=='search':
		html_blocks = re.findall('akoam_result(.*?)<script',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?background-image: url\((.*?)\).*?<h1>(.*?)</h1>',block,re.DOTALL)
		#XBMCGUI_DIALOG_OK(str(len(items)),block)
	elif type=='more':
		html_blocks = re.findall('section_title more_title(.*?)footer_bottom_services',html,re.DOTALL)
	#elif type=='news':
	#	html_blocks = re.findall('section_title news_title(.*?)news_more_choices',html,re.DOTALL)
	else:
		html_blocks = re.findall('navigation(.*?)<script',html,re.DOTALL)
	if not items and html_blocks:
		block = html_blocks[0]
		items = re.findall('div class="subject_box.*?href="(.*?)".*?src="(.*?)".*?<h3.*?>(.*?)</h3>',block,re.DOTALL)
	for link,img,title in items:
		title = title.strip(' ')
		title = unescapeHTML(title)
		if any(value in title for value in noEpisodesLIST): addMenuItem('video',menu_name+title,link,73,img)
		else: addMenuItem('folder',menu_name+title,link,73,img)
	html_blocks = re.findall('class="pagination"(.*?)</ul>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall("</li><li >.*?href='(.*?)'>(.*?)<",block,re.DOTALL)
		for link,title in items:
			addMenuItem('folder',menu_name+'صفحة '+title,link,72,'','',type)
	return

def RESOLVE_UNDERRUN(url):
	html = openURL_cached(LONG_CACHE,url,'',headers,True,'AKOAM-SECTIONS-2nd')
	url2 = re.findall('"href","(.*?)"',html,re.DOTALL)
	url2 = url2[1]
	return url2

def SECTIONS(url):
	#XBMCGUI_DIALOG_OK(url,'SECTIONS 11')
	notvideosLIST = ['zip','rar','txt','pdf','htm','tar','iso','html']
	html = openURL_cached(REGULAR_CACHE,url,'',headers,True,'AKOAM-SECTIONS-1st')
	akwam_link1 = re.findall('"(https*://akwam.net/\w+.*?)"',html,re.DOTALL)
	akwam_link2 = re.findall('"(https*://underurl.com/\w+.*?)"',html,re.DOTALL)
	if akwam_link1 or akwam_link2:
		if akwam_link1: url3 = akwam_link1[0]
		elif akwam_link2: url3 = RESOLVE_UNDERRUN(akwam_link2[0])
		url3 = unquote(url3)
		#XBMCGUI_DIALOG_OK(url3,'SECTIONS 22')
		import AKWAM
		if '/series/' in url3 or '/shows/' in url3: AKWAM.EPISODES(url3)
		else: AKWAM.PLAY(url3)
		return
	ratingLIST = re.findall('محتوى الفيلم.*?>.*?(\w*?)\W*?<',html,re.DOTALL)
	if RATING_CHECK(script_name,url,ratingLIST): return
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	#XBMCGUI_DIALOG_OK(url,html)
	items = re.findall('<br />\n<a href="(.*?)".*?<span style="color:.*?">(.*?)</span>',html,re.DOTALL)
	for link,title in items:
		title = unescapeHTML(title)
		addMenuItem('folder',menu_name+title,link,73)
	html_blocks = re.findall('class="sub_title".*?<h1.*?>(.*?)</h1>.*?class="main_img".*?src="(.*?)".*?ad-300-250(.*?)ako-feedback',html,re.DOTALL)
	if not html_blocks:
		XBMCGUI_DIALOG_NOTIFICATION('خطأ خارجي','لا يوجد ملف فيديو')
		return
	name,img,block = html_blocks[0]
	name = name.strip(' ')
	if 'sub_epsiode_title' in block:
		items = re.findall('sub_epsiode_title">(.*?)</h2>.*?sub_file_title.*?>(.*?)<',block,re.DOTALL)
	else:
		filenames = re.findall('sub_file_title\'>(.*?) - <i>',block,re.DOTALL)
		items = []
		for filename in filenames:
			items.append( ('رابط التشغيل',filename) )
	if not items: items = [ ('رابط التشغيل','') ]
	count = 0
	titleLIST,episodeLIST = [],[]
	size = len(items)
	for title,filename in items:
		filetype = ''
		if ' - ' in filename: filename = filename.split(' - ')[0]
		else: filename = 'dummy.zip'
		if '.' in filename: filetype = filename.split('.')[-1]
		#if any(value in filetype for value in notvideosLIST):
		#	if 'رابط التشغيل' not in title: title = title + ':'
		title = title.strip(' ')
		titleLIST.append(title)
		episodeLIST.append(count)
		count += 1
	#XBMCGUI_DIALOG_OK(str(size),str(episodeLIST))
	if size>0:
		if any(value in name for value in noEpisodesLIST):
			if size==1:
				selection = 0
			else:
				#XBMCGUI_DIALOG_SELECT('',titleLIST)
				selection = XBMCGUI_DIALOG_SELECT('اختر الفيديو المناسب:', titleLIST)
				if selection == -1: return
			PLAY(url+'?section='+str(1+episodeLIST[size-selection-1]))
		else:
			for i in reversed(range(size)):
				#if ':' in titleLIST[i]: title = titleLIST[i].strip(':') + ' - ملف الفيديو غير موجود'
				#else: title = name + ' - ' + titleLIST[i]
				title = name + ' - ' + titleLIST[i]
				link = url + '?section='+str(size-i)
				addMenuItem('video',menu_name+title,link,74,img)
	else:
		addMenuItem('video',menu_name+'الرابط ليس فيديو','',9999,img)
		#XBMCGUI_DIALOG_NOTIFICATION('خطأ خارجي','الرابط ليس فيديو')
	return

def PLAY(url):
	#XBMCGUI_DIALOG_OK(url,'')
	url2,episode = url.split('?section=')
	html = openURL_cached(REGULAR_CACHE,url2,'',headers,True,'AKOAM-PLAY_AKOAM-1st')
	html_blocks = re.findall('ad-300-250.*?ad-300-250(.*?)ako-feedback',html,re.DOTALL)
	html_block = html_blocks[0].replace('\'direct_link_box','"direct_link_box epsoide_box')
	html_block = html_block + 'direct_link_box'
	blocks = re.findall('epsoide_box(.*?)direct_link_box',html_block,re.DOTALL)
	episode = len(blocks)-int(episode)
	block = blocks[episode]
	linkLIST = []
	serversDICT = {'1423075862':'dailymotion','1477487601':'estream','1505328404':'streamango',
		'1423080015':'flashx','1458117295':'openload','1423079306':'vimple','1430052371':'ok.ru',
		'1477488213':'thevid','1558278006':'uqload','1477487990':'vidtodo'}
	items = re.findall('download_btn\' target=\'_blank\' href=\'(.*?)\'',block,re.DOTALL)
	for link in items:
		linkLIST.append(link+'?named=________akoam')
	items = re.findall('background-image: url\((.*?)\).*?href=\'(.*?)\'',block,re.DOTALL)
	for serverIMG,link in items:
		serverIMG = serverIMG.split('/')[-1]
		serverIMG = serverIMG.split('.')[0]
		if serverIMG in serversDICT:
			linkLIST.append(link+'?named='+serversDICT[serverIMG]+'________akoam')
		else: linkLIST.append(link+'?named='+serverIMG+'________akoam')
	#XBMCGUI_DIALOG_SELECT('PLAY AKOAM',linkLIST)
	#return
	if len(linkLIST)==0:
		message = re.findall('sub-no-file.*?\n(.*?)\n',block,re.DOTALL)
		if message: XBMCGUI_DIALOG_OK('رسالة من الموقع الاصلي',message[0])
		else: XBMCGUI_DIALOG_OK('رسالة من المبرمج','لا يوجد ملف فيديو')
	else:
		#XBMCGUI_DIALOG_SELECT('',linkLIST)
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def SEARCH(search):
	#XBMCGUI_DIALOG_OK(search,'')
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','%20')
	#XBMCGUI_DIALOG_OK(str(len(search)) , str(len(new_search)) )
	url = website0a + '/search/'+new_search
	results = TITLES(url,'search')
	return



