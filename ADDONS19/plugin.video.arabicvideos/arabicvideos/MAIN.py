# -*- coding: utf-8 -*-
from LIBRARY import *

script_name = 'MAIN'


type,name99,url99,mode,image99,page99,text,favourite = EXTRACT_KODI_PATH()
mode0 = int(mode)
mode1 = int(mode0%10)
mode2 = int(mode0/10)


#xbmcgui.Dialog().ok('['+menu_path+']','['+mode+']')
#xbmcgui.Dialog().ok('['+menu_label+']','['+menu_path+']')


LOG_THIS('NOTICE','============================================================================================')
#message += '\n'+'Label:['+menu_label+']   Path:['+menu_path+']'
if mode0==260: message = '  Version: [ '+addon_version+' ]  Kodi: [ '+kodi_release+' ]'
else:
	menu_label2 = menu_label.replace('   ','  ').replace('   ','  ').replace('   ','  ')
	menu_path2 = menu_path.replace('   ','  ').replace('   ','  ').replace('   ','  ')
	message = '  Label: [ '+menu_label2+' ]  Mode: [ '+mode+' ]  Path: [ '+menu_path2+' ]'
if favourite not in ['','1','2','3','4','NOREFRESH']:
	message = message+'   .  Favourite: [ '+favourite+' ]'
LOG_THIS('NOTICE',LOGGING(script_name)+message)


UPDATE_RANDOM_MENUS = mode2==16 and mode0 not in [160,165]
UPDATE_RANDOM_SUBMENUS = mode2==16 and 'UPDATE' in text
SEARCH_MODES = mode0 in [19,29,39,49,59,69,79,99,119,139,149,209,229,239,249,259]
SITES_MODES = mode2 in [1,2,3,4,5,6,7,9,11,13,14,20,22,24,25]
IPTV_MODES = mode2==23 and text!=''
YOUTUBE_UPDATE = mode2==14 and 'UPDATE' in text


if favourite not in ['','1','2','3','4','NOREFRESH']:
	import FAVOURITES
	FAVOURITES.FAVOURITES_DISPATCHER(favourite)
	#"Container.Refresh" used because there is no addon_handle number to use for ending directory
	#"Container.Update" used to open a menu list using specific addon_path
	#xbmc.executebuiltin("Container.Update("+sys.argv[0]+addon_path.split('&favourite=')[0]+")")
	if 'NOREFRESH' not in favourite: xbmc.executebuiltin("Container.Refresh")
	EXIT_PROGRAM('MAIN-FAVOURITES-1st',False)


if (SEARCH_MODES and menu_label not in ['..','Main Menu']) or (UPDATE_RANDOM_MENUS and menu_label!='Main Menu'):
	LOG_THIS('NOTICE','  .  Writing random list  .  path: [ '+addon_path+' ]')
	results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,favourite)
	new_menuItemsLIST = []
	for type88,name88,url88,mode88,image88,page88,text88,favourite88 in menuItemsLIST:
		new_menuItemsLIST.append((type88,name88,url88,mode88,image88,page88,text88,'NOREFRESH'))
	newFILE = str(new_menuItemsLIST)
	with open(lastrandomfile,'w') as f: f.write(newFILE)
	menuItemsLIST[:] = new_menuItemsLIST
elif (SEARCH_MODES and menu_label in ['..','Main Menu']) or (UPDATE_RANDOM_MENUS and menu_label=='Main Menu'):
	LOG_THIS('NOTICE','  .  Reading random list  .  path: [ '+addon_path+' ]')
	with open(lastrandomfile,'r') as f: oldFILE = f.read()
	menuItemsLIST[:] = eval(oldFILE)
else: results = MAIN_DISPATCHER(type,name99,url99,mode,image99,page99,text,favourite)


if not os.path.exists(addoncachefolder): os.makedirs(addoncachefolder)
if not os.path.exists(dbfile):
	CLEAN_KODI_CACHE_FOLDER()
	conn = sqlite3.connect(dbfile)
	conn.close()
	import SERVICES
	SERVICES.KODI_SKIN()
	SERVICES.INSTALL_REPOSITORY(False)
	xbmcgui.Dialog().ok('IPTV','تم مسح الكاش أو تحديث البرنامج . فإذا كنت تستخدم IPTV فقم بجلب ملفات IPTV جديدة أو للتخلص من هذه الرسالة ادخل إلى قائمة IPTV وامسح الملفات القديمة')
	import IPTV
	IPTV.CREATE_STREAMS()


#xbmcgui.Dialog().ok(addon_path,str(mode0))


if addon_handle>-1:


	if type=='folder' and menu_label!='..' and (SITES_MODES or IPTV_MODES): ADD_TO_LAST_VIDEO_FILES()

	FILTERING_MENUS = mode0 in [114,204,244,254] and text!=''
	DELETE_LAST_VIDEOS = mode0 in [266,268]

	# kodi defaults
	succeeded,updateListing,cacheToDisc = True,False,True

	if menuItemsLIST:
		KodiMenuList = []
		for menuItem in menuItemsLIST:
			kodiMenuItem = getKodiMenuItem(menuItem)
			KodiMenuList.append(kodiMenuItem)
		addItems_succeeded = xbmcplugin.addDirectoryItems(addon_handle,KodiMenuList)

	if type=='folder' or SEARCH_MODES or UPDATE_RANDOM_SUBMENUS: succeeded = True
	else: succeeded = False

	# updateListing = True => means this list is temporary and will be overwritten by the next list
	# updateListing = False => means this list is permanent and the new list will generate new menu
	if FILTERING_MENUS or DELETE_LAST_VIDEOS or UPDATE_RANDOM_SUBMENUS or YOUTUBE_UPDATE: updateListing = True
	else: updateListing = False
	

	#LOG_THIS('NOTICE',str(succeeded)+'  '+str(updateListing)+'  '+str(cacheToDisc))
	xbmcplugin.endOfDirectory(addon_handle,succeeded,updateListing,cacheToDisc)

	#PLAY_VIDEO_MODES = mode2 in [12,24,33,43,53,63,74,82,92,105,112,123,134,143,182,202,212,223,243,252]
	#xbmcgui.Dialog().ok(str(succeeded),str(updateListing),str(cacheToDisc))
	#xbmcgui.Dialog().ok(addon_path,str(addon_handle))


#xbmcgui.Dialog().ok(str(addon_handle),addon_path)



