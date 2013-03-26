#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, sys, urllib, urllib2, cookielib, time, codecs
import socket
socket.setdefaulttimeout(50)

PLUGIN_NAME   = 'YaTv'
siteUrl = 'm.tv.yandex.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'script.module.YaTv.cookies.sid')

addon = xbmcaddon.Addon(id='script.module.YaTv')
handle = addon.getAddonInfo('id')
__settings__ = xbmcaddon.Addon(id='script.module.YaTv')
thumb = os.path.join( addon.getAddonInfo('path'), "icon.png" )
fanart = os.path.join( addon.getAddonInfo('path'), "fanart.jpg" )
icon = os.path.join( addon.getAddonInfo('path'), 'icon.png')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
#tab="[COLOR 00000000]_[/COLOR]"


def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L


def construct_request(params):
	return '%s?%s' % (sys.argv[0], urllib.urlencode(params))

def htmlEntitiesDecode(string):
	return BeautifulStoneSoup(string, convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))


def GET(target, referer, post=None):
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		print 'HTTP ERROR '+ target


def formtext(http):
	dict={}
	ss='title="'
	es='</table><table class="b'
	Lhttp=mfindal(http, ss, es)
	print "Каналов:"+ str(len(Lhttp))
	for cnl in Lhttp:
		ss='title="'
		es='" alt="'
		nmc=mfindal(cnl, ss, es)[0].replace(ss,"")
		ss="['http://m.tv.yandex.ru"
		es='#end'
		nprg=mfindal(cnl.replace("'",'"').replace('class="time"><a href="',"['http://m.tv.yandex.ru").replace('</a></td><td>',"','").replace('">',"','").replace('</td></tr>',"']#end")+"", ss, es)
		Lprg=[]
		for i in nprg:
			Lprg.append(eval(i))
		dict[nmc]=Lprg
	return dict


def formtext2(http):
	dict={}
	ss='alt="" title="" src="'
	es='" /><div class="b-broadcast__time'
	try:
		img=mfindal(http, ss, es)[0].replace(ss,"")#.replace("middle","orig")
	except:img=""
	ss='b-broadcast__info"><p>'
	es='</p><'
	try:pl=mfindal(http, ss, es)[0].replace(ss,"")
	except: pl=""
	ss='class="b-icon" src="'
	es='orig" title="'
	try:ico=mfindal(http, ss, es)[0].replace(ss,"")+'orig'
	except: ico=""
	return {"img":img,"pl":pl,"ico":ico}


def upd1(rg, ch):
	#categoryUrl = 'http://m.tv.yandex.ru/'+rg+'/channels/'+ch
	categoryUrl = 'http://m.tv.yandex.ru/193?channel=597%2C146%2C823%2C162%2C187%2C515%2C633%2C211%2C246%2C593%2C706%2C427%2C212%2C279%2C318%2C740%2C323%2C557%2C898%2C150%2C916%2C917%2C918%2C919%2C921%2C922%2C924%2C925%2C926%2C927%2C928%2C929%2C932%2C933%2C934%2C935%2C710%2C579%2C658%2C756%2C365%2C516%2C463%2C601%2C828%2C495%2C325%2C409%2C355%2C437%2C60%2C23%2C850%2C288%2C661%2C429%2C575%2C608%2C102%2C312%2C567%2C55%2C127%2C267%2C309%2C589%2C213%2C521%2C277%2C346%2C454%2C669%2C66%2C747%2C834%2C273%2C123%2C798%2C462%2C22%2C71%2C542%2C618%2C675%2C518%2C12%2C485%2C783%2C617%2C566%2C638%2C715%2C743%2C53%2C406%2C663%2C447%2C181%2C777%2C173%2C163%2C794%2C716%2C180%2C779%2C686%2C16%2C284%2C502%2C410%2C659%2C615%2C810%2C520%2C352%2C19%2C494%2C598%2C646%2C51%2C138%2C319%2C741%2C831%2C15%2C801%2C145%2C757%2C82%2C765%2C223%2C461%2C328%2C31%2C631%2C59%2C644%2C37%2C434%2C384%2C648%2C313%2C119%2C125%2C789%2C547%2C156%2C442%2C455%2C333%2C804%2C533%2C604%2C376%2C769%2C25%2C705%2C21%2C642%2C626%2C141%2C637%2C477%2C552%2C247%2C275%2C776%2C555%2C308%2C332%2C849%2C132%2C388%2C39%2C425%2C774%2C258%2C389%2C680%2C591%2C723%2C154%2C331%2C367%2C505%2C595%2C731%2C6%2C737%2C481%2C726%2C423%2C491%2C113%2C713%2C111%2C662%2C201%2C681%2C91%2C322%2C377%2C499%2C134%2C664%2C183%2C697%2C358%2C563%2C311%2C217%2C24%2C799%2C821%2C614%2C153%2C415%2C250%2C8%2C401%2C306%2C554%2C214%2C531%2C851%2C473%2C897%2C412%2C363%2C458%2C151%2C730%2C560%2C178%2C576%2C349%2C165%2C257%2C852%2C923%2C920%2C931%2C930%2C911%2C912%2C983%2C990%2C989%2C986%2C987%2C988%2C984%2C278%2C797%2C393%2C315%2C430%2C431%2C11%2C121%2C807%2C685%2C509%2C464%2C35%2C382%2C270%2C237%2C249&flag=&when=1'
	#categoryUrl = 'http://m.tv.yandex.ru/193?when=1&channel=597%2C146%2C823%2C162%2C187%2C515%2C633%2C211'

	http = GET(categoryUrl, categoryUrl)
	if http == None:
		showMessage('RuTor:', 'Сервер не отвечает', 1000)
		return None
	else:
		d=formtext(http)
		#return d
		save_cache(repr(d))

def upd3(rg, ch):
	#categoryUrl = 'http://m.tv.yandex.ru/193?when=1&channel=597%2C146%2C823%2C162%2C187%2C515%2C633%2C211'
	categoryUrl = 'http://m.tv.yandex.ru/193?channel=597%2C146%2C823%2C162%2C187%2C515%2C633%2C211%2C246%2C593%2C706%2C427%2C212%2C279%2C318%2C740%2C323%2C557%2C898%2C150%2C916%2C917%2C918%2C919%2C921%2C922%2C924%2C925%2C926%2C927%2C928%2C929%2C932%2C933%2C934%2C935%2C710%2C579%2C658%2C756%2C365%2C516%2C463%2C601%2C828%2C495%2C325%2C409%2C355%2C437%2C60%2C23%2C850%2C288%2C661%2C429%2C575%2C608%2C102%2C312%2C567%2C55%2C127%2C267%2C309%2C589%2C213%2C521%2C277%2C346%2C454%2C669%2C66%2C747%2C834%2C273%2C123%2C798%2C462%2C22%2C71%2C542%2C618%2C675%2C518%2C12%2C485%2C783%2C617%2C566%2C638%2C715%2C743%2C53%2C406%2C663%2C447%2C181%2C777%2C173%2C163%2C794%2C716%2C180%2C779%2C686%2C16%2C284%2C502%2C410%2C659%2C615%2C810%2C520%2C352%2C19%2C494%2C598%2C646%2C51%2C138%2C319%2C741%2C831%2C15%2C801%2C145%2C757%2C82%2C765%2C223%2C461%2C328%2C31%2C631%2C59%2C644%2C37%2C434%2C384%2C648%2C313%2C119%2C125%2C789%2C547%2C156%2C442%2C455%2C333%2C804%2C533%2C604%2C376%2C769%2C25%2C705%2C21%2C642%2C626%2C141%2C637%2C477%2C552%2C247%2C275%2C776%2C555%2C308%2C332%2C849%2C132%2C388%2C39%2C425%2C774%2C258%2C389%2C680%2C591%2C723%2C154%2C331%2C367%2C505%2C595%2C731%2C6%2C737%2C481%2C726%2C423%2C491%2C113%2C713%2C111%2C662%2C201%2C681%2C91%2C322%2C377%2C499%2C134%2C664%2C183%2C697%2C358%2C563%2C311%2C217%2C24%2C799%2C821%2C614%2C153%2C415%2C250%2C8%2C401%2C306%2C554%2C214%2C531%2C851%2C473%2C897%2C412%2C363%2C458%2C151%2C730%2C560%2C178%2C576%2C349%2C165%2C257%2C852%2C923%2C920%2C931%2C930%2C911%2C912%2C983%2C990%2C989%2C986%2C987%2C988%2C984%2C278%2C797%2C393%2C315%2C430%2C431%2C11%2C121%2C807%2C685%2C509%2C464%2C35%2C382%2C270%2C237%2C249&flag=&when=1'

	http = GET(categoryUrl, categoryUrl)
	if http == None:
		showMessage('RuTor:', 'Сервер не отвечает', 1000)
		return None
	else:
		d=formtext(http)
		return d


def upd2(categoryUrl):#(rg, pr, ev):
	#categoryUrl = 'http://m.tv.yandex.ru/'+rg+'/program/'+pr+'/event/'+ev
	http = GET(categoryUrl, categoryUrl)
	if http == None:
		print "НЕТ ОТВЕТА ОТ YANDEX"
		return None
	else:
		d=formtext2(http)
		return d

def GetPr():
		print "запрос стр"
		d=get_cache()#upd1("193", "146")
		rez={}
		print "обработка"
		for i in d:
			Title = i
			plot = ""
			k=0
			for j in d[i]:
				k+=1
				if k==1:
					id=j[0].replace("http://m.tv.yandex.ru/","").replace("/program/","").replace("/event/","")
					try:
						dd=get_inf_db(id)[0][0].replace("#z","\\").replace("#y",'"')
						d2=eval(dd)
						img=d2["img"].replace("middle","orig")
						pl=d2["pl"]
						ico=d2["ico"]
						plot = plot +"[B][COLOR FF0084FF]"+ j[1]+"[/COLOR] [COLOR FFFFFFFF]"+j[2]+"[/COLOR][/B][COLOR FF999999]"+chr(10)+pl+"[/COLOR]"+chr(10)
					except: 
						img=""
						pl=""
						ico=""
						plot = plot +"[B][COLOR FF0084FF]"+ j[1]+"[/COLOR] [COLOR FFFFFFFF]"+j[2]+"[/COLOR][/B]"+chr(10)
				else:
					plot = plot +"[B][COLOR FF0084FF]"+ j[1]+"[/COLOR] [COLOR FFFFFFFF]"+j[2]+"[/COLOR][/B]"+chr(10)
			rez[i]={"plot":plot, "img":img, "ico":ico}
		print "возврат"
		return rez

import sqlite3 as db
db_name = os.path.join( addon.getAddonInfo('path'), "move_info.db" )
c = db.connect(database=db_name)
cu = c.cursor()
cu.execute("CREATE TABLE IF NOT EXISTS table1 (db_item VARCHAR(250), i VARCHAR(30), t TIME);")
c.commit()



def add_to_db2(n, item):
		tor_id="n"+n
		cu.execute('INSERT INTO table1 (db_item, i, t) VALUES ("'+item+'", "'+tor_id+'", "'+str(time.time())+'");')
		c.commit()

def clean_db():
	tm=str(time.time()-(5*3600))
	cu.execute('SELECT * FROM table1 WHERE t < '+tm+';')
	c.commit()
	L=cu.fetchall()
	for i in L:
		print i[1]
		id=i[1]
		cu.execute("DROP TABLE IF EXISTS "+id+";")
		c.commit()
	cu.execute("DELETE FROM table1 WHERE t < "+tm+";")
	c.commit()
	cu.execute("VACUUM")
	c.commit()

def save_cache(item):
		item=item.replace("\\","#z").replace('"',"#y")
		cu.execute("DROP TABLE IF EXISTS table2;")
		c.commit()
		cu.execute("CREATE TABLE IF NOT EXISTS table2 (db_item VARCHAR(250), t TIME);")
		c.commit()
		cu.execute('INSERT INTO table2 (db_item, t) VALUES ("'+item+'", "'+str(time.time())+'");')
		c.commit()

def get_cache():
	try:
		cu.execute(str('SELECT db_item FROM table2;'))
		c.commit()
		info = eval(cu.fetchall()[0][0].replace("#z","\\").replace("#y",'"'))
	except: info = None
	return info


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
			cu.execute('INSERT INTO table1 (db_item, i, t) VALUES ("'+tor_id+'", "'+tor_id+'", "'+str(time.time())+'");')
			c.commit()
			#c.close()

def get_inf_db(n):
		tor_id="n"+n
		cu.execute(str('SELECT db_item FROM '+tor_id+';'))
		c.commit()
		info = cu.fetchall()
		#c.close()
		return info


def updb_fast():
		print "---Начинаем обновление ---"
		d=upd3("193", "146")
		for i in d:
					j = d[i][0]
					id=j[0].replace("http://m.tv.yandex.ru/","").replace("/program/","").replace("/event/","")
					try: d2=eval(get_inf_db(id)[0][0].replace("#z","\\").replace("#y",'"'))
					except:
						d2=upd2(j[0])
						xbmc.sleep(200)
						#print repr(d2).replace("\\","#z").replace('"',"#y")
						add_to_db(id, repr(d2).replace("\\","#z").replace('"',"#y"))
		print "---Быстрое обновление завершено---"
		clean_db()

def updb():
		d=upd3("193", "146")
		n=0
		for i in d:
			n+=1
			if n==30: print "ОБНОВЛЕНО 20%"
			if n==120: print "ОБНОВЛЕНО 40%"
			if n==180: print "ОБНОВЛЕНО 60%"
			if n==240: print "ОБНОВЛЕНО 80%"
			for j in d[i]:
					id=j[0].replace("http://m.tv.yandex.ru/","").replace("/program/","").replace("/event/","")
					try: d2=eval(get_inf_db(id)[0][0].replace("#z","\\").replace("#y",'"'))
					except: 
						d2=upd2(j[0])
						xbmc.sleep(300)
						add_to_db(id, repr(d2).replace("\\","#z").replace('"',"#y"))
		print "---Обновление завершено---"

upd1(0, 0)