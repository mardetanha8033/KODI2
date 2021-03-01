# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='SHAHID4U'
headers = { 'User-Agent' : '' }
menu_name='_SHA_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['مسلسلات انمي','الرئيسية','عروض مصارعة','الكل','افلام']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==110: results = MENU(url)
	elif mode==111: results = TITLES(url)
	elif mode==112: results = PLAY(url)
	elif mode==113: results = EPISODES(url)
	elif mode==114: results = FILTERS_MENU(url,'FILTERS___'+text)
	elif mode==115: results = FILTERS_MENU(url,'CATEGORIES___'+text)
	elif mode==119: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('folder',menu_name+'بحث في الموقع','',119,'','','_REMEMBERRESULTS_')
		addMenuItem('folder',menu_name+'فلتر محدد',website0a,115)
		addMenuItem('folder',menu_name+'فلتر كامل',website0a,114)
		#addMenuItem('folder',menu_name+'فلتر','',114,website0a)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,'','SHAHID4U-MENU-1st')
	#DIALOG_OK('no exit',html)
	if '__Error__' not in html:
		html_blocks = re.findall('categories-tabs(.*?)advanced-search',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('data-get="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
		for link,title in items:
			url = website0a+'/getposts?type=one&data='+link
			addMenuItem('folder',website+'___'+menu_name+title,url,111)
		if website=='': addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
		html_blocks = re.findall('navigation-menu(.*?)</div>',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
		if 'افلام عربي' not in str(items):
			addMenuItem('folder',website+'___'+menu_name+'افلام عربي',website0a+'/category/افلام-عربي-1',111)
		for link,title in items:
			if 'javascript' in link: continue
			if 'http' not in link: link = website0a+link
			"""
			if '%' in link:
				link = unquote(link)
				link = link.replace('ه','ة')
				link = link.replace('ى','ي')
			"""
			title = title.strip(' ')
			#if not any(value in title for value in ignoreLIST):
			#	if any(value in title for value in keepLIST):
			if title not in ignoreLIST:
				addMenuItem('folder',website+'___'+menu_name+title,link,111)
	return html

def TITLES(url):
	#DIALOG_OK(url,url)
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'SHAHID4U-TITLES-1st')
	if 'getposts' in url: block = html
	else:
		html_blocks = re.findall('page-content(.*?)tags-cloud',html,re.DOTALL)
		block = html_blocks[0]
	items = re.findall('class="box.*?src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link,title in items:
		if '/series/' in link: continue
		link = unquote(link).strip('/')
		title = unescapeHTML(title)
		title = title.strip(' ')
		if '/film/' in link or any(value in title for value in itemLIST):
			addMenuItem('video',menu_name+title,link,112,img)
		elif '/episode/' in link and 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					addMenuItem('folder',menu_name+title,link,113,img)
					allTitles.append(title)
		else: addMenuItem('folder',menu_name+title,link,113,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href=["\'](http.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if title!='': addMenuItem('folder',menu_name+'صفحة '+title,link,111)
	return

def EPISODES(url):
	episodesCount,items,itemsNEW = -1,[],[]
	html = OPENURL_CACHED(REGULAR_CACHE,url,'',headers,True,'SHAHID4U-EPISODES-1st')
	html_blocks = re.findall('ti-list-numbered(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		itemsNEW = []
		blocks = ''.join(html_blocks)
		items = re.findall('href="(.*?)"',blocks,re.DOTALL)
	items.append(url)
	items = set(items)
	#name = xbmc.getInfoLabel('ListItem.Label')
	for link in items:
		link = link.strip('/')
		title = '_MOD_' + link.split('/')[-1].replace('-',' ')
		sequence = re.findall('الحلقة-(\d+)',link.split('/')[-1],re.DOTALL)
		if sequence: sequence = sequence[0]
		else: sequence = '0'
		itemsNEW.append([link,title,sequence])
	items = sorted(itemsNEW, reverse=False, key=lambda key: int(key[2]))
	seasonsCount = str(items).count('/season/')
	episodesCount = str(items).count('/episode/')
	if seasonsCount>1 and episodesCount>0 and '/season/' not in url:
		for link,title,sequence in items:
			if '/season/' in link: addMenuItem('folder',menu_name+title,link,113)
	else:
		for link,title,sequence in items:
			if '/season/' not in link: addMenuItem('video',menu_name+title,link,112)
	return

def PLAY(url):
	#LOG_THIS('NOTICE','EMAD 111')
	linkLIST = []
	parts = url.split('/')
	#DIALOG_OK(url,'PLAY-1st')
	#url = unquote(quote(url))
	hostname = website0a
	response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url,'',headers,True,True,'SHAHID4U-PLAY-1st')
	html = response.content#.encode('utf8')
	id = re.findall('postId:"(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post_id=(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post-id="(.*?)"',html,re.DOTALL)
	if id: id = id[0]
	else: DIALOG_OK('رسالة من المبرمج','يرجى إرسال هذه المشكلة إلى المبرمج  من قائمة خدمات البرنامج')
	#LOG_THIS('NOTICE','EMAD START TIMING 111')
	if True or '/watch/' in html:
		#parts = url.split('/')
		url2 = url.replace(parts[3],'watch')
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers,True,True,'ARBLIONZ-PLAY-2nd')
		html2 = response.content#.encode('utf8')
		items1 = re.findall('data-embedd="(.*?)".*?alt="(.*?)"',html2,re.DOTALL)
		items2 = re.findall('data-embedd=".*?(http.*?)("|&quot;)',html2,re.DOTALL)
		items3 = re.findall('src=&quot;(.*?)&quot;.*?>(.*?)<',html2,re.DOTALL|re.IGNORECASE)
		items4 = re.findall('data-embedd="(.*?)">\n*.*?server_image">\n(.*?)\n',html2)
		items5 = re.findall('src=&quot;(.*?)&quot;.*?alt="(.*?)"',html2,re.DOTALL|re.IGNORECASE)
		items6 = re.findall('server="(.*?)".*?<span>(.*?)<',html2,re.DOTALL|re.IGNORECASE)
		items = items1+items2+items3+items4+items5+items6
		#LOG_THIS('NOTICE','EMAD START TIMING 444')
		if not items:
			items = re.findall('<span>(.*?)</span>.*?src="(.*?)"',html2,re.DOTALL|re.IGNORECASE)
			items = [(b,a) for a,b in items]
		for server,title in items:
			if '.png' in server: continue
			if '.jpg' in server: continue
			if '&quot;' in server: continue
			quality = re.findall('\d\d\d+',title,re.DOTALL)
			if quality:
				quality = quality[0]
				if quality in title: title = title.replace(quality+'p','').replace(quality,'').strip(' ')
				quality = '____'+quality
			else: quality = ''
			#LOG_THIS('NOTICE','['+str(id)+']  ['+str(hostname)+']  ['+str(title)+']  ['+str(quality)+']')
			if server.isdigit():
				link = hostname+'/?postid='+id+'&serverid='+server+'?named='+title+'__watch'+quality
			else:
				if 'http' not in server: server = 'http:'+server
				quality = re.findall('\d\d\d+',title,re.DOTALL)
				if quality: quality = '____'+quality[0]
				else: quality = ''
				link = server+'?named=__watch'+quality
			linkLIST.append(link)
	#LOG_THIS('NOTICE','['+quality+']    ['+title+']')
	#selection = DIALOG_SELECT('أختر البحث المناسب', linkLIST)
	#DIALOG_OK('watch 1',	str(len(items)))
	if 'DownloadNow' in html:
		headers2 = { 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8' }
		url2 = url.replace(parts[3],'download')
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers2,True,'','SHAHID4U-PLAY-3rd')
		html2 = response.content#.encode('utf8')
		#DIALOG_OK(url2,html2)
		html_blocks = re.findall('<ul class="download-items(.*?)</ul>',html2,re.DOTALL)
		for block in html_blocks:
			items = re.findall('href="(http.*?)".*?<span>(.*?)<.*?<p>(.*?)<',block,re.DOTALL)
			for link,name,quality in items:
				link = link+'?named='+name+'__download'+'____'+quality
				linkLIST.append(link)
	elif '/download/' in html:
		headers2 = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
		url2 = hostname + '/ajaxCenter?_action=getdownloadlinks&postId='+id
		response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url2,'',headers2,True,True,'SHAHID4U-PLAY-4th')
		html2 = response.content#.encode('utf8')
		if 'download-btns' in html2:
			items3 = re.findall('href="(.*?)"',html2,re.DOTALL)
			for url3 in items3:
				if '/page/' not in url3 and 'http' in url3:
					url3 = url3+'?named=__download'
					linkLIST.append(url3)
				elif '/page/' in url3:
					quality = ''
					response = OPENURL_REQUESTS_CACHED(LONG_CACHE,'GET',url3,'',headers,True,True,'SHAHID4U-PLAY-5th')
					html4 = response.content#.encode('utf8')
					blocks = re.findall('(<strong>.*?)-----',html4,re.DOTALL)
					for block4 in blocks:
						server4 = ''
						items4 = re.findall('<strong>(.*?)</strong>',block4,re.DOTALL)
						for item4 in items4:
							item = re.findall('\d\d\d+',item4,re.DOTALL)
							if item:
								quality = '____'+item[0]
								break
						for item4 in reversed(items4):
							item = re.findall('\w\w+',item4,re.DOTALL)
							if item:
								server4 = item[0]
								break
						items5 = re.findall('href="(.*?)"',block4,re.DOTALL)
						for link5 in items5:
							link5 = link5+'?named='+server4+'__download'+quality
							linkLIST.append(link5)
			#DIALOG_OK('download 1',	str(len(linkLIST))	)
		elif 'slow-motion' in html2:
			html2 = html2.replace('<h6 ','==END== ==START==')+'==END=='
			html2 = html2.replace('<h3 ','==END== ==START==')+'==END=='
			#LOG_THIS('NOTICE',html2)
			#with open('s:\\emad.html','w') as f: f.write(html2)
			all_blocks = re.findall('==START==(.*?)==END==',html2,re.DOTALL)
			if all_blocks:
				for block4 in all_blocks:
					if 'href=' not in block4: continue
					#DIALOG_OK('download 111',	block4	)
					quality4 = ''
					items4 = re.findall('slow-motion">(.*?)<',block4,re.DOTALL)
					for item4 in items4:
						item = re.findall('\d\d\d+',item4,re.DOTALL)
						if item:
							quality4 = '____'+item[0]
							break
					items4 = re.findall('<td>(.*?)</td>.*?href="(http.*?)"',block4,re.DOTALL)
					if items4:
						for server4,link4 in items4:
							link4 = link4+'?named='+server4+'__download'+quality4
							linkLIST.append(link4)
					else:
						items4 = re.findall('href="(.*?http.*?)".*?name">(.*?)<',block4,re.DOTALL)
						for link4,server4 in items4:
							link4 = link4.strip(' ')+'?named='+server4+'__download'+quality4
							linkLIST.append(link4)
			else:
				items4 = re.findall('href="(.*?)".*?>(\w+)<',html2,re.DOTALL)
				for link4,server4 in items4:
					link4 = link4.strip(' ')+'?named='+server4+'__download'
					linkLIST.append(link4)
	#LOG_THIS('NOTICE','EMAD 222')
	#DIALOG_OK('both: watch & download',	str(len(linkLIST))	)
	#selection = DIALOG_SELECT('أختر البحث المناسب', linkLIST)
	if len(linkLIST)==0: DIALOG_OK('رسالة من المبرمج','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name,'video')
	return

def SEARCH(search):
	search,options,showdialogs = SEARCH_OPTIONS(search)
	if search=='': search = KEYBOARD()
	if search=='': return
	search = search.replace(' ','+')
	html = OPENURL_CACHED(LONG_CACHE,website0a,'',headers,True,'SHAHID4U-SEARCH-1st')
	html_blocks = re.findall('chevron-select(.*?)</div>',html,re.DOTALL)
	if showdialogs and html_blocks:
		block = html_blocks[0]
		items = re.findall('value="(.*?)".*?>(.*?)<',block,re.DOTALL)
		categoryLIST,filterLIST = [],[]
		for category,title in items:
			if title in ['عروض مصارعة']: continue
			categoryLIST.append(category)
			filterLIST.append(title)
		selection = DIALOG_SELECT('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
	else: category = ''
	url = website0a + '/search?s='+search+'&category='+category
	TITLES(url)
	return

def FILTERS_MENU(url,filter):
	filter = filter.replace('_FORGETRESULTS_','')
	#DIALOG_OK(filter,url)
	menu_list = ['category','genre','release-year']
	if '?' in url: url = url.split('/getposts?')[0]
	type,filter = filter.split('___',1)
	if filter=='': filter_options,filter_values = '',''
	else: filter_options,filter_values = filter.split('___')
	if type=='CATEGORIES':
		if menu_list[0]+'=' not in filter_options: category = menu_list[0]
		for i in range(len(menu_list[0:-1])):
			if menu_list[i]+'=' in filter_options: category = menu_list[i+1]
		new_options = filter_options+'&'+category+'=0'
		new_values = filter_values+'&'+category+'=0'
		new_filter = new_options.strip('&')+'___'+new_values.strip('&')
		clean_filter = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		url2 = url+'/getposts?'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		if filter_values=='': url2 = url
		else: url2 = url+'/getposts?'+filter_values
		addMenuItem('folder',menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url2,111)
		addMenuItem('folder',menu_name+' [[   '+filter_show+'   ]]',url2,111)
		addMenuItem('link','[COLOR FFC89008]====================[/COLOR]','',9999)
	html = OPENURL_CACHED(LONG_CACHE,url,'',headers,True,'SHAHID4U-FILTERS_MENU-1st')
	html_blocks = re.findall('<form class(.*?)</form>',html,re.DOTALL)
	block = html_blocks[0]
	select_blocks = re.findall('select.*?<a.*?>(.*?)</a>.*?data-tax="(.*?)"(.*?)</ul>',block,re.DOTALL)
	#DIALOG_OK('',str(select_blocks))
	dict = {}
	for name,category2,block in select_blocks:
		name = name.replace('--','')
		items = re.findall('data-cat="(.*?)".*?checkmark-bold">(.*?)<',block,re.DOTALL)
		if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES___'+new_filter)
				return
			else:
				if category2==menu_list[-1]: addMenuItem('folder',menu_name+'الجميع ',url2,111)
				else: addMenuItem('folder',menu_name+'الجميع ',url2,115,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'___'+new_values
			addMenuItem('folder',menu_name+'الجميع :'+name,url2,114,'','',new_filter+'_FORGETRESULTS_')
		dict[category2] = {}
		for value,option in items:
			if option in ignoreLIST: continue
			#if 'value' not in value: value = option
			#else: value = re.findall('"(.*?)"',value,re.DOTALL)[0]
			dict[category2][value] = option
			new_options = filter_options+'&'+category2+'='+option
			new_values = filter_values+'&'+category2+'='+value
			new_filter2 = new_options+'___'+new_values
			title = option+' :'#+dict[category2]['0']
			title = option+' :'+name
			if type=='FILTERS': addMenuItem('folder',menu_name+title,url,114,'','',new_filter2+'_FORGETRESULTS_')
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				url3 = url+'/getposts?'+clean_filter
				addMenuItem('folder',menu_name+title,url3,111)
			else: addMenuItem('folder',menu_name+title,url,115,'','',new_filter2)
	return

def RECONSTRUCT_FILTER(filters,mode):
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER 11')
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	filters = filters.replace('=&','=0&')
	filters = filters.strip('&')
	filtersDICT = {}
	if '=' in filters:
		items = filters.split('&')
		for item in items:
			var,value = item.split('=')
			filtersDICT[var] = value
	new_filters = ''
	url_filter_list = ['quality','release-year','genre','category']
	for key in url_filter_list:
		if key in filtersDICT.keys(): value = filtersDICT[key]
		else: value = '0'
		if '%' not in value: value = quote(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&'+key+'='+value
		elif mode=='all': new_filters = new_filters+'&'+key+'='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&')
	new_filters = new_filters.replace('=0','=')
	#DIALOG_OK(filters,'RECONSTRUCT_FILTER 22')
	return new_filters

