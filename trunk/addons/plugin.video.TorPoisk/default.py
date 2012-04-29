#!/usr/bin/python
# -*- coding: utf-8 -*-

# *      Copyright (C) 2011 TDW
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# */
import time

import httplib
import urllib
import urllib2
import re
import sys
import os
import Cookie

import string, xbmc, xbmcgui, xbmcplugin, os, urllib, cookielib, xbmcaddon, time, codecs

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import socket
socket.setdefaulttimeout(50)

#---------libtorrents-torrenter-by-slng---
try:import Downloader
except: pass
def playTorrent(url, StorageDirectory):
		torrentUrl = url#__settings__.getSetting("lastTorrent")
		if 0 != len(torrentUrl):
			contentId = 0#int(urllib.unquote_plus(url))
			torrent = Downloader.Torrent(torrentUrl, StorageDirectory)
			torrent.startSession(contentId)
			iterator = 0
			progressBar = xbmcgui.DialogProgress()
			progressBar.create('Подождите', 'Идёт поиск сидов.')
			while not torrent.canPlay:
				time.sleep(0.1)
				progressBar.update(iterator)
				iterator += 1
				if iterator == 100:
					iterator = 0
				if progressBar.iscanceled():
					progressBar.update(0)
					progressBar.close()
					return
			progressBar.update(0)
			progressBar.close()
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			listitem = xbmcgui.ListItem(torrent.getContentList()[contentId].path)
			playlist.add(torrent.getFilePath(contentId), listitem)
			progressBar.close()
			xbmc.Player().play(playlist)
			progressBar.close()
			while 1 == xbmc.Player().isPlayingVideo():
				torrent.fetchParts()
				torrent.checkThread()
				time.sleep(1)
			xbmc.executebuiltin("Notification(%s, %s)" % ('Информация', 'Загрузка торрента прекращена.'))
			torrent.threadComplete = True
		else:
			print " Unexpected access to method playTorrent() without torrent content"



#---------tsengine----by-nuismons-----

from tsengine import TSengine

from urllib import unquote, quote

hos = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

__addon__ = xbmcaddon.Addon( id = 'plugin.video.TorPoisk' )
#__language__ = __addon__.getLocalizedString

addon_icon    = __addon__.getAddonInfo('icon')
#addon_fanart  = __addon__.getAddonInfo('fanart')
#addon_path    = __addon__.getAddonInfo('path')
addon_type    = __addon__.getAddonInfo('type')
addon_id      = __addon__.getAddonInfo('id')
addon_author  = __addon__.getAddonInfo('author')
addon_name    = __addon__.getAddonInfo('name')
addon_version = __addon__.getAddonInfo('version')

# JSON понадобится, когда будет несколько файлов в торренте
try:
	import json
except ImportError:
	try:
		import simplejson as json
		xbmc.log( '[%s]: Error import json. Uses module simplejson' % addon_id, 2 )
	except ImportError:
		try:
			import demjson3 as json
			xbmc.log( '[%s]: Error import simplejson. Uses module demjson3' % addon_id, 3 )
		except ImportError:
			xbmc.log( '[%s]: Error import demjson3. Sorry.' % addon_id, 4 )

def construct_request(params):
	return '%s?%s' % (sys.argv[0], urllib.urlencode(params))

def showMessage(heading, message, times = 3000, pics = addon_icon):
	try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading.encode('utf-8'), message.encode('utf-8'), times, pics.encode('utf-8')))
	except Exception, e:
		xbmc.log( '[%s]: showMessage: Transcoding UTF-8 failed [%s]' % (addon_id, e), 2 )
		try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, times, pics))
		except Exception, e:
			xbmc.log( '[%s]: showMessage: exec failed [%s]' % (addon_id, e), 3 )

class myPlayer(xbmc.Player):
	def __init__( self, *args, **kwargs ):
		self.active = True
		self.playl=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		self.playl.clear()
		self.title='None'
		
	def playlist_add( self, url, it):
		self.playl.add(url=url, listitem= it)
		
	def play_start(self, ind=0):
		self.play(self.playl)
		self.playselected(ind)

	def onPlayBackEnded( self ):
		self.active = False
	def onPlayBackStopped( self ):
		self.active = False
		
			


def play(torr_link):

	#torr_link=params['torr_url']	
	
	TSplayer=TSengine(addon_icon)
	#TSplayer.end()
		
	if not TSplayer.connect():
		li = xbmcgui.ListItem('TSengine не запущен!!')
		uri = construct_request({
			'func': 'mainScreen'
		})
		xbmcplugin.addDirectoryItem(hos, uri, li, False)
		xbmcplugin.endOfDirectory(hos)
		exit
	
	while not TSplayer.ready:
		time.sleep(1)
		
	TSplayer.load(torr_link)
	
	while not TSplayer.filelist:
		time.sleep(1)
	

	if TSplayer.file_count>1:
		TSplayer.end()
		#showMessage('Торренты', 'Больше 1', 2000)
		files=json.loads(TSplayer.filelist)

		for list in files['files']:
			li = xbmcgui.ListItem(urllib.unquote(list[0]))
#			uri = construct_request({
#				'torr_url': torr_link,
#				'title': list[0],
#				'ind':list[1],
#				'func': 'playlist'
#			})
			uri = sys.argv[0] + '?mode=Playlist'\
				+ '&url=' + urllib.quote_plus(torr_link)\
				+ '&num=' + urllib.quote_plus(str(list[1]))\
				+ '&title=' + urllib.quote_plus(list[0])
#				+ '&info=' + urllib.quote_plus(repr(dict))\
			xbmcplugin.addDirectoryItem(hos, uri, li, False)
		xbmcplugin.endOfDirectory(hos)
		
	else:
		files=json.loads(TSplayer.filelist)
		list=files['files'][0]
		li = xbmcgui.ListItem(list[0].decode())
		uri = sys.argv[0] + '?mode=Playlist'\
				+ '&url=' + urllib.quote_plus(torr_link)\
				+ '&num=' + urllib.quote_plus(str(list[1]))\
				+ '&title=' + urllib.quote_plus(list[0])
		xbmcplugin.addDirectoryItem(hos, uri, li, False)
		xbmcplugin.endOfDirectory(hos)
		link=TSplayer.geturl_ind()

		plr=myPlayer()
		lit= xbmcgui.ListItem(params['title'], thumbnailImage=None)
		plr.playlist_add(link, lit)
		plr.play_start()
	
		while plr.active:
			xbmc.sleep(500)
		
		TSplayer.end()
		showMessage('Торрент', 'Стоп', 2000)              


def TSplaylist(torr_link, ind):

	#torr_link=params['torr_url']	
	
	TSplayer=TSengine(addon_icon)
		
	if not TSplayer.connect():
		li = xbmcgui.ListItem('TSengine не запущен!!')
		uri = construct_request({
			'func': 'mainScreen'
		})
		xbmcplugin.addDirectoryItem(hos, uri, li, False)
		xbmcplugin.endOfDirectory(hos)
		exit
		
	while not TSplayer.ready:
		time.sleep(1)
		
	TSplayer.load(torr_link)
	
	while not TSplayer.filelist:
		time.sleep(1)
	link=TSplayer.geturl_ind(int(ind))

	plr=myPlayer()
	lit= xbmcgui.ListItem(urllib.unquote(params['title']), thumbnailImage='http://s017.radikal.ru/i437/1111/87/90c2ae0f6220.jpg')
	plr.playlist_add(link, lit)
	plr.play_start(int(ind))
	
	while plr.active:
		xbmc.sleep(500)
		
	TSplayer.end()
	showMessage('Торрент', 'Стоп', 2000)

#--------------------------

icon = xbmc.translatePath(os.path.join(os.getcwd().replace(';', ''), 'icon.png'))
siteUrl = 'www.rutor.org'
httpSiteUrl = 'http://' + siteUrl
#sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'plugin.video.TorPoisk.cookies.sid')

h = int(sys.argv[1])

def construct_request(params):
	return '%s?%s' % (sys.argv[0], urllib.urlencode(params))

def htmlEntitiesDecode(string):
	return BeautifulStoneSoup(string, convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

headers  = {
	'User-Agent' : 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.7.62 Version/11.00',
	'Accept'     :' text/html, application/xml, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*',
	'Accept-Language':'ru-RU,ru;q=0.9,en;q=0.8',
	'Accept-Charset' :'utf-8, utf-16, *;q=0.1',
	'Accept-Encoding':'identity, *;q=0'
}

def GET(target, referer, post_params = None, accept_redirect = True, get_redirect_url = False, siteUrl='www.rutor.org'):
	try:
		connection = httplib.HTTPConnection(siteUrl)

		if post_params == None:
			method = 'GET'
			post = None
		else:
			method = 'POST'
			post = urllib.urlencode(post_params)
			headers['Content-Type'] = 'application/x-www-form-urlencoded'
		
		sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'plugin.video.rutor.cookies.sid')
		if os.path.isfile(sid_file):
			fh = open(sid_file, 'r')
			csid = fh.read()
			fh.close()
			headers['Cookie'] = 'session=%s' % csid

		headers['Referer'] = referer
		connection.request(method, target, post, headers = headers)
		response = connection.getresponse()

		if response.status == 403:
			raise Exception("Forbidden, check credentials")
		if response.status == 404:
			raise Exception("File not found")
		if accept_redirect and response.status in (301, 302):
			target = response.getheader('location', '')
			if target.find("://") < 0:
				target = httpSiteUrl + target
			if get_redirect_url:
				return target
			else:
				return GET(target, referer, post_params, False)

		try:
			sc = Cookie.SimpleCookie()
			sc.load(response.msg.getheader('Set-Cookie'))
			fh = open(sid_file, 'w')
			fh.write(sc['session'].value)
			fh.close()
		except: pass

		if get_redirect_url:
			return False
		else:
			http = response.read()
			return http

	except Exception, e:
		showMessage('Error', e, 5000)
		return None





def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
	
handle = int(sys.argv[1])

PLUGIN_NAME   = 'TorPoisk'

addon = xbmcaddon.Addon(id='plugin.video.TorPoisk')
__settings__ = xbmcaddon.Addon(id='plugin.video.TorPoisk')
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

#dc={"1 канал" : "001", "1+1" : "002"}
try:
	from KPmenu import*
except:
	pass

thumb = os.path.join( addon.getAddonInfo('path'), "icon.png" )
fanart = os.path.join( addon.getAddonInfo('path'), "fanart.jpg" )
LstDir = os.path.join( addon.getAddonInfo('path'), "playlists" )
dbDir = os.path.join( addon.getAddonInfo('path'), "db" )
ImgPath = os.path.join( addon.getAddonInfo('path'), "logo" )
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

#siteUrl = '109.95.47.77/BP-TV.m3u'
#httpSiteUrl = 'http://' + siteUrl
#httpSiteUrl = 'http://opensharing.org/download/43651'
#httpSiteUrl ='http://d.rutor.org/download/175775'

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

def showMessage(heading, message, times = 50000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, thumb))



def GET2(url):
	try:
		urllib.urlretrieve(url,os.path.join(LstDir, "KP.html"))
		#print 'def GET(%s):'%url
		req = urllib2.Request(url)
		f = urllib2.urlopen(req)
		a = f.read()
		f.close()
		return a
	except:
		showMessage('Не могу открыть URL def GET', url)
		return None

def cleartext(str):
	str=str.replace('</td><td ><a class="downgif" href="',"', '")
	str=str.replace('"><img src="http://s.rutor.org/i/d.gif" alt="D" /></a><a href="magnet:?xt=',"', '")
	str=str.replace('alt="M" /></a><a href="/torrent/',"', '")
	str=str.replace('</a></td> <td align="right">',"', '")
	str=str.replace('<img src="http://s.rutor.org/i/com.gif" alt="C" /></td><td align="right">',"', '")
	str=str.replace('</td><td align="center"><span class="green"><img src="http://s.rutor.org/t/arrowup.gif" alt="S" />',"', '")
	str=str.replace('</span><img src="http://s.rutor.org/t/arrowdown.gif" alt="L" /><span class="red">',"', '")
	str=str.replace('">',"', '")
	str=str.replace('</span></td></tr>',"']")
	str=str.replace('</span>',"']")
	str=str.replace("</table>", "\r")
	return str

def formtext(http):
	http=http.replace(chr(10),"")#.replace(chr(13),"")
	
	http=http.replace('&#039;',"").replace('colspan = "2"',"").replace('&nbsp;',"") #исключить
	http=http.replace('</td></tr><tr class="gai"><td>',"\rflag1 ['") 
	http=http.replace('</td></tr><tr class="gai">',"\rflag1 ") #начало
	#http=http.replace('/></a>\r<a href',' *** ').replace('alt="C" /></td>\r<td align="right"',' *** ') #склеить
	http=http.replace('<tr class="tum"><td>',"\rflag1 ['").replace('<tr class="gai"><td>',"\rflag1 ['") #разделить
	http=cleartext(http)
	return http
	#fl = open(os.path.join( ru(LstDir),"test.txt"), "w")
	#fl.write(http)
	#fl.close()

def inputbox():
	skbd = xbmc.Keyboard()
	skbd.setHeading('Поиск:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return ""

def upd(category, sort, text):
	if text=='0':
		stext=""
	else:
		stext=xt(text)#inputbox()
	stext=stext.replace("%", "%20").replace(" ", "%20").replace("?", "%20").replace("#", "%20")
	if stext=="":
		categoryUrl = xt('http://www.rutor.org/browse/0/'+category+'/0/'+sort)
	else:
		categoryUrl = 'http://www.rutor.org/search/0/'+category+'/000/'+sort+'/'+stext   #)xt(
	http = GET(categoryUrl, httpSiteUrl, None, True, False, 'www.rutor.org')
	if http == None:
		showMessage('RuTor:', 'Сервер не отвечает', 1000)
		return None
	else:
		http=formtext(http)
		LL=http.splitlines()
		return LL

def debug(s):
	fl = open(os.path.join( ru(LstDir),"test.txt"), "w")
	fl.write(s)
	fl.close()

def formtext2(http):
	#http=http.replace(chr(10),"")#.replace(chr(13),"")
	http=http.replace(chr(13),chr(10))
	
	http=http.replace("    "," ")
	http=http.replace("    "," ")
	http=http.replace("   "," ")
	http=http.replace("   "," ")
	http=http.replace("  "," ")
	http=http.replace("  "," ")
	n=http.find("function getLevel() { return 48; }")
	k=http.rfind('<select class="navigator_per_page">')
	http=http[n:k]
	http=http.replace("'",'^')
	http=http.replace('13px; font-weight: bold" href="',chr(10)+"flag1: ['")
	http=http.replace('" class="all">',"', '")
	http=http.replace('</a><span style="color: #888; font-family: arial; font-size: 11px; display: block">',"', '")
	http=http.replace('<nobr>',"', '")
	http=http.replace('</nobr></span></div>',"']")
	
	http=http.replace('title="/images',chr(10)+"flag2:")
	http=http.replace('" style="border',chr(10))
	
	http=http.replace('<br />'+chr(10)+' (', chr(10)+"flag3: ")
	http=http.replace('...)', "")
	http=http.replace(')'+chr(10), chr(10))
	http=http.replace('&nbsp;', " ")
	http=http.replace('&#233;', 'é')
	#http=http.replace('&laquo;', '«')
	#http=http.replace('&raquo;', '»')
	http=http.replace('&laquo;', '"')
	http=http.replace('&raquo;', '"')

	http=p.sub('', http)
	#debug(http)
	return http

def KP(nType, nGenre, Rating, nYar, nCantry):
	if nCantry=='0':cantry=''
	else:cantry='country%5D/'+str(nCantry)+'/m_act%5B'
	if nYar=='0':decad=''
	else:decad='decade%5D/'+nYar+'/'
	Rating=str(Rating)
	if nGenre==0: nGenre=''
	else: nGenre='genre%5D/'+str(nGenre)+'/m_act%5B'#+","
	if nType=='all': gn=''
	else:gn='m_act%5B'+nType+"%5D/on/"
	httpUrl="http://www.kinopoisk.ru"
	#Url = xt('http://www.kinopoisk.ru/level/48/m_act%5Bgenre%5D/2/m_act%5Bnum_vote%5D/500/m_act%5Brating%5D/7:/order/rating/#results')
	Url = xt('http://www.kinopoisk.ru/level/48/m_act%5B'+nGenre+cantry+decad+'num_vote%5D/350/m_act%5Brating%5D/'+Rating+':/'+gn+'order/rating/perpage/200/#results')
	http = GET(Url, httpUrl, None, True, False, 'www.kinopoisk.ru')
	if http == None:
		showMessage('kinopoisk:', 'Сервер не отвечает', 1000)
		return None
	else:
		http=formtext2(http)
		LL=http.splitlines()
		return LL


def format(L):
	if L==None: 
		return ["","","","","","","","",""]
	else:
		Ln=[]
		i=0
		for itm in L:
			i+=1
			if len(itm)>6:
				if itm[:5]=="flag1": Ln.append(eval(itm[6:]))
		return Ln


def format2(L):
	if L==None: 
		return ["","","","","","","","",""]
	else:
		LL=[]
		Ln=[]
		L1=[]
		L2=""
		L3=""
		RG=""
		RT=""
		IMDB=""
		i=0
		for itm in L:
			i+=1
			if len(itm)>6:
				if itm[:5]=="flag2": L2=itm[6:]
				if itm[:5]=="flag1": L1=eval(itm[6:])
				if itm[:5]==" реж.": RG=itm[6:]
				if itm[:5]=="flag3": L3=itm[6:]
				if itm[:5]==" rati": RT=itm[8:12]
				if itm[:5]==" IMDb": 
					IMDB=itm[7:11]
					Ln=L1
					Ln.append(L2)
					Ln.append(L3)
					Ln.append(RG)
					Ln.append(RT)
					Ln.append(IMDB)
					LL.append(Ln)
		debug(str(LL))
		return LL


ru_film='5'
en_film='1'
nauka='12'
serial='4'
tv_video='6'
mult='7'
anime='10'
all_cat='0'

sort_data='0'
sort_sid='2'
sort_name='6'

LCantry=[]

def SetCantry (LType, nType, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, nYar, YarLabel, LCantry, n, CantryLabel):
		for i in CantryList:
			if i[0] == n: Title = '   ['+xt(chr(149))+'] '+ i[1]
			else: Title = '   [_] '+ i[1]
			row_url = Title
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus('1')\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&LCantry=' + urllib.quote_plus(repr(LCantry))\
				+ '&nCantry=' + urllib.quote_plus(repr(i[0]))\
				+ '&CantryLabel=' + urllib.quote_plus(i[1])\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

LType=[]
def SetType(LType, n, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, nYar, YarLabel):
		#if n in LType: LType.remove(n)
		#else: LType.append(n)
		for i in TypeList:
			if i[0] == n: Title = '   ['+xt(chr(149))+'] '+ i[1]
			else: Title = '   [_] '+ i[1]
			row_url = Title
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(i[0]))\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus('1')\
				+ '&TypeLabel=' + urllib.quote_plus(i[1])\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

LGenre=[]
def SetGenre(LType, nType, TypeLabel, LGenre, n, GenreLabel, Rating, LYar, nYar, YarLabel):
		for i in GenreList:
			if i[0] == int(n): Title = '   ['+xt(chr(149))+'] '+ i[1]
			else: Title = '   [_] '+ i[1]
			row_url = Title
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(i[0]))\
				+ '&GenreLabel=' + urllib.quote_plus(i[1])\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&gnr=' + urllib.quote_plus('1')\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

def SetYar(LType, nType, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, n, YarLabel ):
		#if n in LType: LType.remove(n)
		#else: LType.append(n)
		for i in YarList:
			if i[0] == n: Title = '   ['+xt(chr(149))+'] '+ i[1]
			else: Title = '   [_] '+ i[1]
			row_url = Title
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&dec=' + urllib.quote_plus('1')\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(i[0]))\
				+ '&YarLabel=' + urllib.quote_plus(i[1])\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)


def ShowRoot(cat, gnr, LType, nType, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, nYar, YarLabel, dec, can, LCantry, nCantry, CantryLabel):
	#if nType in LType: LType.remove(nType)
	#else: LType.append(nType)
	
	if 1==1:
			Title = "[ Категория: "+ TypeLabel +" ]"
			row_url = '1'
			if cat=='0': cat='1'
			else: cat='0'
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(en_film)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus(cat)\
				+ '&gnr=' + urllib.quote_plus('1')\
				+ '&dec=' + urllib.quote_plus('1')\
				+ '&can=' + urllib.quote_plus('1')\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&LCantry=' + urllib.quote_plus(repr(LCantry))\
				+ '&nCantry=' + urllib.quote_plus(repr(nCantry))\
				+ '&CantryLabel=' + urllib.quote_plus(CantryLabel)\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)
	
	if cat=='1':SetType(LType, nType, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, nYar, YarLabel)
	
	#if str(nGenre) in LGenre: LGenre.remove(str(nGenre))
	#else: LGenre.append(str(nGenre))
	if 1==1:
			Title = "[ Жанр: "+ GenreLabel +" ]"
			row_url = Title
			if gnr=='0': gnr='1'
			else: gnr='0'
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(en_film)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus('1')\
				+ '&gnr=' + urllib.quote_plus(gnr)\
				+ '&dec=' + urllib.quote_plus('1')\
				+ '&can=' + urllib.quote_plus('1')\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&LCantry=' + urllib.quote_plus(repr(LCantry))\
				+ '&nCantry=' + urllib.quote_plus(repr(nCantry))\
				+ '&CantryLabel=' + urllib.quote_plus(CantryLabel)\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

	if gnr=='1':SetGenre(LType, nType, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, nYar, YarLabel)

	if 1==1:
			Title = "[ Произведено в: "+ YarLabel +" ]"
			row_url = Title
			if dec=='0': dec='1'
			else: dec='0'
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(en_film)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus('1')\
				+ '&gnr=' + urllib.quote_plus('1')\
				+ '&dec=' + urllib.quote_plus(dec)\
				+ '&can=' + urllib.quote_plus('1')\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&LCantry=' + urllib.quote_plus(repr(LCantry))\
				+ '&nCantry=' + urllib.quote_plus(repr(nCantry))\
				+ '&CantryLabel=' + urllib.quote_plus(CantryLabel)\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

	if dec=='1':SetYar(LType, nType, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, nYar, YarLabel)

	if 1==1:
			Title = "[ Страна: "+ CantryLabel +" ]"
			row_url = Title
			if can=='0': can='1'
			else: can='0'
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(en_film)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus('1')\
				+ '&gnr=' + urllib.quote_plus('1')\
				+ '&dec=' + urllib.quote_plus('1')\
				+ '&can=' + urllib.quote_plus(can)\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&LCantry=' + urllib.quote_plus(repr(LCantry))\
				+ '&nCantry=' + urllib.quote_plus(repr(nCantry))\
				+ '&CantryLabel=' + urllib.quote_plus(CantryLabel)\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

	if can=='1':SetCantry(LType, nType, TypeLabel, LGenre, nGenre, GenreLabel, Rating, LYar, nYar, YarLabel, LCantry, nCantry, CantryLabel)


	if 1==1:
			row_url = '1'
			Rating=int(Rating)
			if Rating<10: Rating+=1
			else: Rating=5
			Title = "[ Оценка: "+ str(Rating) +" ]"
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Root'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(en_film)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus('1')\
				+ '&gnr=' + urllib.quote_plus('1')\
				+ '&dec=' + urllib.quote_plus('1')\
				+ '&can=' + urllib.quote_plus('1')\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&LCantry=' + urllib.quote_plus(repr(LCantry))\
				+ '&nCantry=' + urllib.quote_plus(repr(nCantry))\
				+ '&CantryLabel=' + urllib.quote_plus(CantryLabel)\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

	if 1==1:
			Title = " ___________________________________________ "
			row_url = Title
			if gnr=='0': gnr='1'
			else: gnr='0'
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Search'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(en_film)\
				+ '&sort=' + urllib.quote_plus('2')\
				+ '&cat=' + urllib.quote_plus('1')\
				+ '&gnr=' + urllib.quote_plus(gnr)\
				+ '&dec=' + urllib.quote_plus('1')\
				+ '&can=' + urllib.quote_plus('1')\
				+ '&LType=' + urllib.quote_plus(repr(LType))\
				+ '&nType=' + urllib.quote_plus(repr(nType))\
				+ '&LGenre=' + urllib.quote_plus(repr(LGenre))\
				+ '&nGenre=' + urllib.quote_plus(repr(nGenre))\
				+ '&GenreLabel=' + urllib.quote_plus(GenreLabel)\
				+ '&TypeLabel=' + urllib.quote_plus(TypeLabel)\
				+ '&LYar=' + urllib.quote_plus(repr(LYar))\
				+ '&nYar=' + urllib.quote_plus(repr(nYar))\
				+ '&YarLabel=' + urllib.quote_plus(YarLabel)\
				+ '&LCantry=' + urllib.quote_plus(repr(LCantry))\
				+ '&nCantry=' + urllib.quote_plus(repr(nCantry))\
				+ '&CantryLabel=' + urllib.quote_plus(CantryLabel)\
				+ '&Rating=' + urllib.quote_plus(str(Rating))\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)
			
	exs=cat+gnr+dec+can
	exs=exs.replace("0","")
	expand=len(exs)
	if expand==1:Search('', '', 'text', nType, nGenre, Rating, nYar, nCantry)
		

		#catv=(1,0,0,0)
		#i=0
		#for itm in TypeList:
		#	i+=1
		#	Title = itm[1]
		#	row_url = Title
		#	listitem = xbmcgui.ListItem(Title)
		#	listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
		#	purl = sys.argv[0] + '?mode=Root'\
		#		+ '&url=' + urllib.quote_plus(row_url)\
		#		+ '&title=' + urllib.quote_plus(Title)\
		#		+ '&category=' + urllib.quote_plus(all_cat)\
		#		+ '&sort=' + urllib.quote_plus(sort_sid)\
		#		+ '&cat=' + urllib.quote_plus(cat)\
		#		+ '&text=' + urllib.quote_plus('0')
		#	xbmcplugin.addDirectoryItem(handle, purl, listitem, True)
			
			

#---- по сидам ----
#http://rutor.org/search/0/12/000/2/ -- Науч поп
#http://rutor.org/search/0/5/000/2/ -- ru
#http://rutor.org/search/0/1/000/2/ -- en
#http://rutor.org/search/0/4/000/2/ -- serial
#http://rutor.org/search/0/6/000/2/ -- tv
#http://rutor.org/search/0/7/000/2/ -- mult
#http://rutor.org/search/0/10/000/2/ -- anime
#http://rutor.org/search/0/0/000/2/ -- all

#------- по дате
#http://rutor.org/search/0/0/000/0/

#---- по сидам ---- 2  cn 0
#http://rutor.org/browse/0/0/0/2 - 1 str all
#http://rutor.org/browse/0/1/0/2 - en
#http://rutor.org/browse/0/4/0/2 - serial
#
#---- по дате ---
#http://rutor.org/browse/0/4/0/0 - serial

#abc
#http://rutor.org/browse/0/4/0/6
#
p = re.compile(r'<.*?>')
#p.sub('', html)

def clearinfo2(str):
	str=str.replace(chr(13)+chr(10),chr(10))
	str=str.replace(chr(10)+chr(13),chr(10))
	
	str=str.replace('<b>',"").replace('</b>',"")
	str=str.replace('<i>',"").replace('</i>',"")
	str=str.replace('<u>',"").replace('</u>',"")
	str=str.replace('<tr>',"").replace('</tr>',"")
	str=str.replace('<td>',"").replace('</td>',"")
	str=str.replace('<table>',"").replace('</table>',"")
	str=str.replace('<a',"").replace('</a>',"")
	str=str.replace('<br />',"")
	str=str.replace('<hr />',"")
	str=str.replace('<li> ',"")
	str=str.replace('</span>',"")
	str=str.replace('<font size="3">',"").replace('</font>',"")
	str=str.replace('<font size="4">',"")
	str=str.replace('<font size="5">',"")
	
	str=str.replace('<span style="color:chocolate;">',"")
	str=str.replace('<span style="color:green;">',"")
	str=str.replace('<span style="color:indigo;">',"")
	str=str.replace('<span style="color:blue;">',"")
	str=str.replace('<span style="color:maroon;">',"")
	str=str.replace('<span style="color:brown;">',"")
	str=str.replace('<span style="color:darkgreen;">',"")
	
	str=str.replace("<td class='header'>","")
	
	#str=str.replace('<img src="',chr(10)+'Обложка: "')
	#str=str.replace('<td style="vertical-align:top;"><img src="', 'Обложка: "')
	str=str.replace(' style="float:right;" />',"")
	str=str.replace('" />','"')
	
	str=str.replace('О фильме:'+chr(10), chr(10)+'О фильме: ')
	str=str.replace('О фильме: '+chr(10), chr(10)+'О фильме: ')
	str=str.replace('О фильме:  '+chr(10), chr(10)+'О фильме: ')
	str=str.replace('О фильме:   '+chr(10), chr(10)+'О фильме: ')
	
	str=str.replace('<div class="hidewrap"><div class="hidehead" onclick="hideshow($(this))">',"")
	str=str.replace('</div><div class="hidebody"></div><textarea class="hidearea"> href="',': ["')
	str=str.replace('<td class="header">',"")
	str=str.replace(' /></textarea></div>',"]")
	str=str.replace('</textarea></div>',"]")
	str=str.replace(' target="_blank"><img src=',",")
	str=str.replace('"'+chr(10)+'<img src="', "','")
	str=str.replace(' />  href=',",")
	str=str.replace('"  href="',",")
	str=str.replace('href="/tag/7/" target="_blank">',"")
	str=str.replace('href="/tag/6/" target="_blank">',"")
	str=str.replace('href="/tag/5/" target="_blank">',"")
	str=str.replace('href="/tag/4/" target="_blank">',"")
	str=str.replace('href="/tag/3/" target="_blank">',"")
	str=str.replace('href="/tag/2/" target="_blank">',"")
	str=str.replace('href="/tag/1/" target="_blank">',"")
	
	str=str.replace('О фильме:',chr(10)+"О фильме:")
	str=str.replace('Год выхода:',chr(10)+"Год выхода:")
	str=str.replace('Описание:',chr(10)+"Описание:")
	str=str.replace('Название:',chr(10)+"Название:")
	str=str.replace('Жанр:',chr(10)+"Жанр:")
	str=str.replace('Режиссер:',chr(10)+"Режиссер:")
	#n=str.find("http://mediaget.com/torrent")
	n=str.find('<table id="details">')
	k=str.rfind("Сидер замечен")
	str=str[n:k]
	try:
		i=str.find('Информация о фильме')
		j=str.find('.jpg')
		k=str.find('.png')
		if i>0: 
			tmp=str[:i]
			i2=tmp.rfind('.')+4
			i1=tmp.rfind('http:')
			tmp=tmp[i1:i2]
			ext=tmp[-3:]
			if ext=="jpe":tmp=tmp+"g"
			str=str.replace('Информация о фильме', chr(10)+'Обложка: "'+tmp+'"')
		elif j>0:
			tmp=str[:j+4]
			i1=tmp.rfind('http:')
			tmp=tmp[i1:]
			str=chr(10)+'Обложка: "'+tmp+'"'+chr(10)+str
		elif k>0:
			tmp=str[:k+4]
			i1=tmp.rfind('http:')
			tmp=tmp[i1:]
			str=chr(10)+'Обложка: "'+tmp+'"'+chr(10)+str
		else:
			str=str.replace('<img src="', chr(10)+'Обложка: "',1)
	except:
		str=str.replace('<img src="', chr(10)+'Обложка: "',1)
	str=p.sub('', str)
	return str


def clearinfo(str):
	n=str.find('<table id="details">')
	k=str.rfind("Сидер замечен")
	str=str[n:k]
	str=str.replace(chr(13)+chr(10),chr(10))
	str=str.replace(chr(10)+chr(13),chr(10))
	str=str.replace(chr(13),chr(10))
	
	str=str.replace('Год выхода:',chr(10)+"Год выхода:")
	str=str.replace('Год выпуска',chr(10)+"Год выхода:")
	str=str.replace('Описание:',chr(10)+"Описание:")
	str=str.replace('Краткое описание:',chr(10)+"Описание:")
	str=str.replace('О фильме:',chr(10)+"Описание:")
	str=str.replace('Название:',chr(10)+"Название:")
	str=str.replace('Жанр:',chr(10)+"Жанр:")
	str=str.replace('Режиссер:',chr(10)+"Режиссер:")

	try:
		i=str.find('Информация о фильме')
		if i<0:
			m=str.find('Год выхода')
			if m>0:
				s=str[:m]
				j=s.find('.jpg')
				k=s.find('.png')
				n=s.find('jpeg')
			else:
				j=str.find('.jpg')
				k=str.find('.png')
				n=str.find('jpeg')
		if i>0:
			tmp=str[:i]
			i2=tmp.rfind('.')+4
			i1=tmp.rfind('http:')
			tmp=tmp[i1:i2]
			ext=tmp[-3:]
			if ext=="jpe":tmp=tmp+"g"
			str=str.replace('Информация о фильме', chr(10)+'Обложка: '+tmp+chr(10))
		elif j>0:
			tmp=str[:j+4]
			i1=tmp.rfind('http:')
			tmp=tmp[i1:]
			str=chr(10)+'Обложка: '+tmp+chr(10)+str
		elif k>0:
			tmp=str[:k+4]
			i1=tmp.rfind('http:')
			tmp=tmp[i1:]
			str=chr(10)+'Обложка: '+tmp+chr(10)+str
		elif n>0:
			tmp=str[:n+4]
			i1=tmp.rfind('http:')
			tmp=tmp[i1:]
			str=chr(10)+'Обложка: '+tmp+chr(10)+str
		else:
			str=str.replace('<img src="', chr(10)+'Обложка: ',1)
	except:
		str=str.replace('<img src="', chr(10)+'Обложка: ',1)

	str=p.sub('', str)
	
	str=str.replace(chr(10)+chr(10)+chr(10),chr(10))
	str=str.replace(chr(10)+chr(10),chr(10))
	str=str.replace('   ',' ')
	str=str.replace('  ',' ')
	str=str.replace('О фильме:'+chr(10), chr(10)+'О фильме: ')
	str=str.replace('О фильме: '+chr(10), chr(10)+'О фильме: ')
	str=str.replace('Описание:'+chr(10), chr(10)+'Описание: ')
	str=str.replace('Описание: '+chr(10), chr(10)+'Описание: ')
	str=str.replace('Оценка',chr(10)+"Оценка: ")
	str=str.replace('.jpg', ".jpg"+chr(10))
	str=str.replace('.jpeg', ".jpeg"+chr(10))
	str=str.replace('.png', ".png"+chr(10))
	
	return str




#move_info_db={}
#try:
#	if move_info_db=={}: from moveinfo_db import*
#except:pass

import sqlite3 as db
db_name = os.path.join( addon.getAddonInfo('path'), "move_info.db" )
c = db.connect(database=db_name)
cu = c.cursor()

def add_to_db(n, item):
		err=0
		tor_id="n"+n
		litm=str(len(item))
		try:
			cu.execute("CREATE TABLE "+tor_id+" (db_item VARCHAR("+litm+"), i VARCHAR(1));")
			c.commit()
		except: err=1
			#print "Ошибка БД"
		if err==0:
			cu.execute('INSERT INTO '+tor_id+' (db_item, i) VALUES ("'+item+'", "1");')
			c.commit()
			#c.close()

def get_inf_db(n):
		#import sqlite3 as db
		#db_name = os.path.join( addon.getAddonInfo('path'), "move_info.db" )
		#c = db.connect(database=db_name)
		#cu = c.cursor()
		tor_id="n"+n
		cu.execute(str('SELECT db_item FROM '+tor_id+';'))
		c.commit()
		info = cu.fetchall()
		#c.close()
		return info




def get_minfo(ntor):
			
			try: dict=eval(xt(get_inf_db(ntor)[0][0]))#dbi = move_info_db[ntor]
			except: #dbi = None
			
			#if dbi == None:
				hp = GET('http://www.rutor.org/torrent/'+ntor, httpSiteUrl, None)
				hp=clearinfo(hp)
				LI=hp.splitlines()
				dict={}
				cover=''
				for itm in LI:
					nc=itm.find(':')
					flag=itm[:nc]
					if flag=='Обложка': 
						cvr=itm.strip()
						dict['cover']=itm[nc+1:].strip()
					elif flag=='Название': dict['title']=itm[nc+1:].strip()
					elif flag=='Оценка': 
						nr=itm.find('из')
						try:
							dict['rating']=float(itm[nc+2:nr])
							#dict['votes']=str(int(int(itm[nc+2:nr])/2))
						except: pass
					elif flag=='Год выхода':
						try:dict['year']=int(itm.strip()[nc+1:])
						except: 
							try:dict['year']=int(itm.strip()[nc+1:nc+6])
							except: pass
					elif flag=='Жанр': dict['genre']=itm[nc+1:].strip()
					elif flag=='Режиссер': dict['director']=itm[nc+1:].strip()
					elif flag=='В ролях': 
						dict['cast']=itm[nc+1:].split(",")[:6]
					elif flag=='О фильме' or flag=='Описание': 
						dict['plot']=formating(itm[nc+1:].strip())[:1000]
						
				#move_info_db[ntor]=dict
				try:add_to_db(ntor, epr(dict))
				except:
					try:add_to_db(ntor, repr(dict).replace('"',"'"))
					except: pass

				if 1==0:
					
					fl = open(os.path.join( ru(dbDir), ntor+".py"), "w")
					fl.write('move_info_db['+ntor+']='+str(dict))
					fl.close()
				
			#else:
				#dict=move_info_db[ntor]
			#print eval(get_inf_db(ntor)[0][0])
			return dict

def Search(category, sort, text, nType, nGenre, Rating, nYar, nCantry):
	RL=KP(nType, nGenre, Rating, nYar, nCantry)
	RootList=format2(RL)
	k=0
	for tTitle in RootList:
		#if len(tTitle)==9:
		#	tTitle.insert(6," ")
		
		if len(tTitle)>0:
			
			size=tTitle[7]
			if len(size)==3:size=size.center(10)
			elif len(size)==4:size=size.center(9)
			elif len(size)==5:size=size.center(8)
			elif len(size)==6:size=size.center(8)
			title=tTitle[1]
			genre=tTitle[5]
			cover="http://st.kinopoisk.ru/images"+tTitle[4]
			cover=cover.replace('images/sm_','images/')
			n=tTitle[2].rfind("(")
			k=tTitle[2].rfind(")")
			try:year=int(tTitle[2][n+1:k])
			except:year=None
			try:rating=float(tTitle[8])
			except:rating=None
			duration=tTitle[3][:-4]
			plot="Название (рус.):   "+xt(tTitle[1]) +chr(10)+"Название (ориг.): "+xt(tTitle[2])+chr(10)+"Длительность:     "+xt(tTitle[3])+ chr(10)+ "Рейтинг KPoisk:    "+xt(tTitle[7])+ chr(10)+ "Рейтинг IMdB:       "+xt(tTitle[8])
			
			ortitle = tTitle[2].strip()
			kn=ortitle.find("(")
			ortitle=ortitle[:kn-1]
			ortitle=ortitle.strip()
			
			SortName = __settings__.getSetting("SortName")
			
			if ortitle[:1] =="(" or SortName=='1': 
				ortitle=tTitle[1]
				kn=ortitle.find("(")
				if kn>0: ortitle=ortitle[:kn-1]
				ortitle=ortitle.strip()
			ortitle=ortitle.replace('^',"'")
			
			dict={'cover':cover, 'title':title, 'genre':genre, 'plot':plot ,'year':year, 'rating':rating, 'duration':duration}
			
			
			Title = "|"+size+"|  "+tTitle[1].strip()#+"I"+ortitle+"I"
			if 1==1:
				row_url = tTitle[0]
				listitem = xbmcgui.ListItem(Title, thumbnailImage=cover, iconImage=cover)
				try:listitem.setInfo(type = "Video", infoLabels = dict)
				except: pass
				listitem.setProperty('fanart_image', cover)
				purl = sys.argv[0] + '?mode=Search2'\
					+ '&url=' + urllib.quote_plus(row_url)\
					+ '&title=' + urllib.quote_plus(Title)\
					+ '&info=' + urllib.quote_plus(repr(dict))\
					+ '&category=' + urllib.quote_plus(all_cat)\
					+ '&sort=' + urllib.quote_plus('2')\
					+ '&text=' + urllib.quote_plus(ortitle)

				xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

def Search2(category, sort, text):
	HideScr = __settings__.getSetting("Hide Scr")
	HideTSnd = __settings__.getSetting("Hide TSound")
	TitleMode = __settings__.getSetting("Title Mode")
	RL=upd(category, sort, text)
	RootList=format(RL)
	if text == '0222':
			Title = "[Поиск]"
			row_url = Title
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Search'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(category)\
				+ '&sort=' + urllib.quote_plus(sort_sid)\
				+ '&text=' + urllib.quote_plus('1')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)
			
			Title = "[Новые]"
			row_url = Title
			listitem = xbmcgui.ListItem(Title)
			listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
			purl = sys.argv[0] + '?mode=Search'\
				+ '&url=' + urllib.quote_plus(row_url)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&category=' + urllib.quote_plus(category)\
				+ '&sort=' + urllib.quote_plus(sort_data)\
				+ '&text=' + urllib.quote_plus('0')
			xbmcplugin.addDirectoryItem(handle, purl, listitem, True)
	k=0
	for tTitle in RootList:
		if len(tTitle)==9:
			tTitle.insert(6," ")
		
		if len(tTitle)==10 and int(tTitle[8])>0:
			
			size=tTitle[7]
			if size[-2:]=="MB":size=size[:-5]+"MB"
			
			if len(size)==3:size=size.center(10)
			elif len(size)==4:size=size.center(9)
			elif len(size)==5:size=size.center(8)
			elif len(size)==6:size=size.center(8)
			
			if len(tTitle[8])==1:sids=tTitle[8].center(9)
			elif len(tTitle[8])==2:sids=tTitle[8].center(8)
			elif len(tTitle[8])==3:sids=tTitle[8].center(7)
			elif len(tTitle[8])==4:sids=tTitle[8].center(6)
			else:sids=tTitle[8]
			
			#------------------------------------------------
			k+=1
			if k<2:
				nnn=tTitle[1].rfind("/")+1
				ntor=xt(tTitle[1][nnn:])
				dict=get_minfo(ntor)
				try:dict=get_minfo(ntor)
				except:dict={}
				try:cover=dict["cover"]
				except:cover=""
				
			#-------------------------------------------------
			
			Title = "|"+sids+"|"+size+"|  "+tTitle[5]
			
			if HideScr == 'true':
				nH1=Title.find("CAMRip")
				nH2=Title.find(") TS")
				nH3=Title.find("CamRip")
				nH4=Title.find(" DVDScr")
				nH=nH1+nH2+nH3+nH4
			else:
				nH=-1
				
			if HideTSnd == 'true':
				sH=Title.find("Звук с TS")
			else:
				sH=-1
				
			if TitleMode == '1': 
				k1=Title.find('/')
				if k1<0: k1=Title.find('(')
				tmp1=Title[:k1]
				n1=Title.find('(')
				k2=Title.find(' от ')
				if k2<0: k2=None
				tmp2=Title[n1:k2]
				Title = tmp1+tmp2
				Title = Title.replace("| Лицензия","")
				Title = Title.replace("| лицензия","")
				Title = Title.replace("| ЛицензиЯ","")
			
			if nH<0 and sH<0:
				row_url = tTitle[1]
				listitem = xbmcgui.ListItem(Title, thumbnailImage=cover, iconImage=cover)
				try:listitem.setInfo(type = "Video", infoLabels = dict)
				except: pass
				listitem.setProperty('fanart_image', cover)
				purl = sys.argv[0] + '?mode=OpenCat'\
					+ '&url=' + urllib.quote_plus(row_url)\
					+ '&title=' + urllib.quote_plus(Title)\
					+ '&info=' + urllib.quote_plus(repr(dict))
				xbmcplugin.addDirectoryItem(handle, purl, listitem, True)
	


def open_pl(pl_name):
	line=""
	Lurl=[]
	Ltitle=[]
	Lnum=[]
	tvlist = os.path.join(LstDir, pl_name+'.txt')
	fl = open(tvlist, "r")
	n=0
	for line in fl.xreadlines():
		n+=1
		if len(line)>5:
			pref=line[:5]
			Lurl.append(ru(line).replace(u'\n','').replace(u'\r',''))
			Lurl.append(ru(line).replace(u'\n','').replace(u'\r',''))
			Lnum.append(len(Lurl)-1)
	fl.close()
	return (Ltitle, Lurl, Lnum)

def formating(str):
	
	str=str.replace('а','a')
	str=str.replace('е','e')
	str=str.replace('ё','e')
	str=str.replace('о','o')
	str=str.replace('р','p')
	str=str.replace('с','c')
	str=str.replace('х','x')
	
	str=str.replace('А','A')
	str=str.replace('Е','E')
	str=str.replace('К','K')
	str=str.replace('М','M')
	str=str.replace('Н','H')
	str=str.replace('О','O')
	str=str.replace('Р','P')
	str=str.replace('С','C')
	str=str.replace('Т','T')
	str=str.replace('Х','X')

	return str



def OpenCat(url, name, dict):
	nnn=url.rfind("/")+1
	ntor=xt(url[nnn:]+".torrent")
	rtpath=ru(os.path.join(LstDir, ntor))
	xtpath=xt(os.path.join(LstDir, ntor))
	try:
		urllib.urlretrieve(xt(url),rtpath)
	except:
		urllib.urlretrieve(xt(url),xtpath)
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.load(xtpath)
	Ltitle, Lurl, Lnum = [],[],[]
	n=0
	
	for i in range (len(playlist)):
		p=playlist[i]
		n+=1
		Ltitle.append(p.getdescription())
		Lurl.append(p.getfilename())
		Lnum.append(n-1)
		
	lgl=(Ltitle, Lurl, Lnum)
	for i in range (len(Ltitle)):
		#Title = formating(Ltitle[i])
		row_name = Ltitle[i]
		row_url = Lurl[i]
		try:cover=dict["cover"]
		except:cover=""
		listitem = xbmcgui.ListItem(row_name, thumbnailImage=cover, iconImage=cover )
		try:listitem.setInfo(type = "Video", infoLabels = dict)
		except: pass
		listitem.setProperty('fanart_image',cover)
		purl = sys.argv[0] + '?mode=OpenPage'\
			+ '&url=' + urllib.quote_plus(row_url)\
			+ '&fanart_image=' + urllib.quote_plus(cover)\
			+ '&num=' + urllib.quote_plus(str(Lnum[i]))\
			+ '&lgl=' + urllib.quote_plus(repr(lgl))\
			+ '&title=' + urllib.quote_plus(Ltitle[i])\
			+ '&info=' + urllib.quote_plus(repr(dict))
		xbmcplugin.addDirectoryItem(handle, purl, listitem, False)



xplayer=xbmc.Player(xbmc.PLAYER_CORE_AUTO)
if os.path.isdir("d:\\TorrentStream")==1: TSpath="d:\\TorrentStream\\"
elif os.path.isdir("c:\\TorrentStream")==1: TSpath="c:\\TorrentStream\\"
elif os.path.isdir("e:\\TorrentStream")==1: TSpath="e:\\TorrentStream\\"
elif os.path.isdir("f:\\TorrentStream")==1: TSpath="f:\\TorrentStream\\"
elif os.path.isdir("g:\\TorrentStream")==1: TSpath="g:\\TorrentStream\\"
elif os.path.isdir("h:\\TorrentStream")==1: TSpath="h:\\TorrentStream\\"
else: TSpath="C:\\"
	
	
def OpenPage(url, name, num, Lgl, dict):
	Ltitle, Lurl, Lnum = Lgl
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	try:thumb2=dict["cover"]
	except:thumb2=""
	for i in range(num,len(Lnum)):
		item = xbmcgui.ListItem(Ltitle[i], iconImage = thumb2, thumbnailImage = thumb2)
		item.setInfo(type="Video", infoLabels=dict)
		playlist.add(url=Lurl[i], listitem=item, index=-1)
	xplayer.play(playlist)
	showMessage('RuTor:', "Соединение...", 100)
	time.sleep(0.3)
	
	for i in range(0,num):
		item = xbmcgui.ListItem(Ltitle[i], iconImage = thumb2, thumbnailImage = thumb2)
		item.setInfo(type="Video", infoLabels=dict)
		playlist.add(url=Lurl[i], listitem=item, index=-1)
	p = xplayer.isPlayingVideo()
	ttl=0
	bsz=0
	while xplayer.isPlayingVideo() == 0 and ttl<20 :
	#for i in range(0,30):
		p = xplayer.isPlayingVideo()
		d = os.path.isfile(TSpath+name)
		
		if d==0:
			showMessage('RuTor:', "[COLOR FFFFF000]Поиск пиров...[/COLOR]", 100)
			ttl+=1
		elif p==0:
			sz=os.path.getsize(TSpath+name)
			pbr="I"*int(sz/(1048576*1.5))
			showMessage("[COLOR FF00FF00]Буферизация: "+str(int(sz/1048576))+" Mb[/COLOR]", "[COLOR FF00FFFF]"+pbr[:51]+"[/COLOR]",100)
			if bsz==sz: ttl+=1
			else: ttl=0
			bsz=sz
		elif p==1:
			return 0
		time.sleep(1)
		


params = get_params()
mode     = None
url      = ''
title    = ''
ref      = ''
img      = ''
num      = 0
category = '0'
sort     = '2'
text     = '0'
Lgl      = ()
info  = {}
move_info_db={}

cat='1'
gnr='1'
dec='1'
can='1'



TypeLabel='ВСЕ'
LType=[]
nType='all'

GenreLabel='ЛЮБОЙ'
LGenre=[]
nGenre=0

YarLabel='ЛЮБОМ ГОДУ'
LYar=[]
nYar='0'

CantryLabel='ЛЮБАЯ'
LCantry=[]
nCantry='0'

Rating='6'

try:
	mode  = urllib.unquote_plus(params["mode"])
except:
	pass

try:
	url  = urllib.unquote_plus(params["url"])
except:
	pass

try:
	title  = urllib.unquote_plus(params["title"])
except:
	pass
try:
	img  = urllib.unquote_plus(params["img"])
except:
	pass
try:
	num  = int(urllib.unquote_plus(params["num"]))
except:
	pass
	
try:
	category  = urllib.unquote_plus(params["category"])
except:
	pass
try:
	sort  = urllib.unquote_plus(params["sort"])
except:
	pass

try:
	text  = urllib.unquote_plus(params["text"])
except:
	pass

try:
	Lgl  = eval(urllib.unquote_plus(params["lgl"]))
except:
	pass

try:
	info  = eval(urllib.unquote_plus(params["info"]))
except:
	pass

try:
	cat  = urllib.unquote_plus(params["cat"])
except:
	pass

try:
	gnr  = urllib.unquote_plus(params["gnr"])
except:
	pass

try:
	dec  = urllib.unquote_plus(params["dec"])
except:
	pass

try:
	can  = urllib.unquote_plus(params["can"])
except:
	pass

try:
	LType  = eval(urllib.unquote_plus(params["LType"]))
except:
	pass

try:
	nType  = eval(urllib.unquote_plus(params["nType"]))
except:
	pass

try:
	TypeLabel  = urllib.unquote_plus(params["TypeLabel"])
except:
	pass
	
try:
	LGenre  = eval(urllib.unquote_plus(params["LGenre"]))
except:
	pass

try:
	nGenre  = eval(urllib.unquote_plus(params["nGenre"]))
except:
	pass

try:
	GenreLabel  = urllib.unquote_plus(params["GenreLabel"])
except:
	pass

try:
	LYar  = eval(urllib.unquote_plus(params["LYar"]))
except:
	pass

try:
	nYar  = eval(urllib.unquote_plus(params["nYar"]))
except:
	pass

try:
	YarLabel  = urllib.unquote_plus(params["YarLabel"])
except:
	pass

try:
	LCantry  = eval(urllib.unquote_plus(params["LCantry"]))
except:
	pass

try:
	nCantry  = eval(urllib.unquote_plus(params["nCantry"]))
except:
	pass

try:
	CantryLabel  = urllib.unquote_plus(params["CantryLabel"])
except:
	pass


try:
	Rating  = urllib.unquote_plus(params["Rating"])
except:
	pass


#xplayer.play("torrentstream:")#C:\Users\Diman\AppData\Roaming\XBMC\addons\plugin.video.RuTor\playlists\179278.torrent 0")
#xplayer.stop()


if mode == None:
	#showMessage("heading", cat, 2000)
	ShowRoot(cat,gnr,LType,nType,TypeLabel,LGenre, nGenre,GenreLabel,Rating, LYar, nYar, YarLabel,dec, can, LCantry, nCantry, CantryLabel)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Root":
	#showMessage("heading", cat, 2000)
	ShowRoot(cat,gnr,LType,nType,TypeLabel,LGenre, nGenre,GenreLabel,Rating, LYar, nYar, YarLabel, dec, can, LCantry, nCantry, CantryLabel)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle, True, True)

if mode == "Playlist":
	TSplaylist(url, num)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "SetType2":
	SetType(LType, nType)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle, True, True)

elif mode == 'Search':
	#xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')
	#try: from moveinfo_db import*
	#except:pass
	Search(category, sort, text, nType, nGenre, Rating, nYar)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
	
	#fl = codecs.open(os.path.join( ru(addon.getAddonInfo('path')), "moveinfo_db.py"), "w",'utf8','ignore')
	#fl.write('# -*- coding: utf-8 -*-'+chr(10))
	#elm=str(move_info_db).encode('utf8','ignore')
	#fl.write('move_info_db='+elm)
	#fl.close()
	
elif mode == 'Search2':
	Search2(category, sort, text)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
	
elif mode == 'OpenCat':
	Engine = __settings__.getSetting("Engine")
	if Engine=="0":play(url)
	elif Engine=="2":playTorrent(url, LstDir)
	else: OpenCat(url, title, info)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

elif mode == 'OpenPage':
	OpenPage(url, title, num, Lgl, info)

c.close()