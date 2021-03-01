# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='CIMANOW'
headers = { 'User-Agent' : '' }
menu_name='_CMN_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==300: results = MENU(url)
	elif mode==301: results = TITLES(url,text)
	elif mode==302: results = PLAY(url)
	elif mode==309: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='': addMenuItem('folder',menu_name+'بحث في الموقع','',309,'','','_REMEMBERRESULTS_')
	#addMenuItem('folder',menu_name+'فلتر','',114,website0a)
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',website0a,'',headers,'','','CIMANOW-MENU-1st')
	html = response.content
	html_blocks = re.findall('class="filter"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('data-filter="(.*?)".*?</i>(.*?)<',block,re.DOTALL)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	for key,title in items:
		title = title.strip(' ')
		url = website0a+'/wp-content/themes/CimaNow/Interface/filter.php'
		addMenuItem('folder',website+'___'+menu_name+title,url,301,'','',key)
	if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html_blocks = re.findall('class="mainMenu"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	ignoreLIST = ['DMCA','الرئيسية']
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		#if any(value in title for value in keepLIST):
		if not any(value in title for value in ignoreLIST):
			addMenuItem('folder',website+'___'+menu_name+title,link,301)
	return html

def TITLES(url,key=''):
	#DIALOG_OK(url,html)
	url = unquote(url)
	if 'الحلقة' in url:
		response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','CIMANOW-TITLES-1st')
		html = response.content
		html_blocks = re.findall('class="SeriesPR"(.*?)class="related"',html,re.DOTALL)
		block = html_blocks[0]
		links = re.findall('href="(.*?)"',block,re.DOTALL)
		url = links[2]
		url = unquote(url)
		#DIALOG_OK(url,'')
	if 'filter.php' in url:
		headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
		data = {'key':key}
		response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'POST',url,data,headers,'','','CIMANOW-TITLES-2nd')
		block = response.content
	else:
		response = OPENURL_REQUESTS_CACHED(REGULAR_CACHE,'GET',url,'','','','','CIMANOW-TITLES-3rd')
		html = response.content
		html_blocks = re.findall('class="results"(.*?)class="footer-menu"',html,re.DOTALL)
		if html_blocks: block = html_blocks[0]
		else:
			new_url = re.findall('<span>[\r\n]+<a href="(.*?)"',html,re.DOTALL)
			TITLES(new_url[2])
			return
	items = re.findall('href="(.*?)".*?class="backg".*?url\((.*?)\).*?class="titleBoxSing">(.*?)<',block,re.DOTALL)
	allTitles = []
	for link,img,title in items:
		title = unescapeHTML(title)
		if '/selary/' in link: addMenuItem('folder',menu_name+title,link,301,img)
		elif '/?s=' in url and 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					addMenuItem('folder',menu_name+title,link,301,img)
					allTitles.append(title)
		else: addMenuItem('video',menu_name+title,link,302,img)
	html_blocks = re.findall('class="pagination"(.*?)</div>',block,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<li><a href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			addMenuItem('folder',menu_name+'صفحة '+title,link,301)
	return

def PLAY(url):
	linkLIST = []
	#DIALOG_OK(url,'')
	#response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url,'','','','','CIMANOW-PLAY-1st')
	#html = response.content
	#url2 = re.findall('redirect=(.*?)"',html,re.DOTALL)
	#if url2: url2 = base64.b64decode(url2[0])
	#else: 
	url2 = url+'watch'
	response = OPENURL_REQUESTS_CACHED(SHORT_CACHE,'GET',url2,'','','','','CIMANOW-PLAY-2nd')
	html2 = response.content
	# watch links
	html_blocks = re.findall('class="watch"(.*?)</ul>',html2,re.DOTALL)
	block = html_blocks[0]
	postid = re.findall("'id': (.*?),",block,re.DOTALL)[0]
	link = re.findall('url: "(.*?)"',block,re.DOTALL)[0]
	items = re.findall('data-server="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for serverid,title in items:
		title = title.strip(' ')
		if title=='Cima Now': title = 'CimaNow'
		#DIALOG_OK(title,'')
		link2 = link+'?postid='+postid+'&serverid='+serverid+'?named='+title+'__watch'
		linkLIST.append(link2)
	# download links
	html_blocks = re.findall('class="download"(.*?)</ul>.</div>',html2,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?<span>(.*?)</span>',block,re.DOTALL)
	for link,title in items:
		title = title.strip(' ')
		quality = re.findall('\d\d\d+',title,re.DOTALL)
		if quality:
			quality = '____'+quality[0]
			title = 'cimanow'
		else: quality = ''
		link2 = link+'?named='+title+'__download'+quality
		linkLIST.append(link2)
	#selection = DIALOG_SELECT('أختر البحث المناسب',linkLIST)
	#LOG_THIS('NOTICE',str(linkLIST))
	if len(linkLIST)==0:
		DIALOG_OK('رسالة من المبرمج','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	url = website0a + '/?s='+search
	TITLES(url)
	return



