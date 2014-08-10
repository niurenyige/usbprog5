#encoding:utf-8
import os
import sys
import subprocess
import json
from collections import defaultdict

code=[]
vendorlen=5
namelen=0
def readfile():

	global vendorlen
	global namelen
	print "readfile"
	try:
		
		i=0
		with open("./processors.txt",'r') as r:
			lines=r.readlines()
			for line in lines:	
				temp=json.loads(line)
				if len(temp['name'])>namelen:
					namelen=len(temp['name'])
				if len(temp['vendor'])>vendorlen:
					vendorlen=len(temp['vendor'])
				if temp['name']!="":
					code.append(temp)
					i=i+1
			print code
				
		
		return code
	except Exception as e: 
			print "error"
			print e
    			exc_type, exc_obj, exc_tb = sys.exc_info()
    			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    			print(exc_type, fname, exc_tb.tb_lineno)		
	return 'error'

def parseavr():
	#namelen=0
	global namelen
	template={"processor":"","name":"","vendor":"Atmel","program":"avrdude"}
	
	with open("./avrdude.conf",'r') as r:
		out=r.read()
	old="!"
	codeav=[]
	i=0
	while old!=out :
		old=out		
		weg, ignored , out =out.partition('#------------------------')
		weg, ignored , out =out.partition('part')
		weg, ignored , out =out.partition('= "')
		tempid, ignored , out =out.partition('";')
		weg, ignored , out =out.partition('= "')
		tempname, ignored , out =out.partition('";')
		#print tempid,tempname
		temp=template
		
		temp['processor']=tempid
		temp['name']=tempname
		line=json.dumps(temp)
		temp=json.loads(line)
		i=0
	
		if unicode("u'"+temp['name']+"',") in unicode(code):
			#print "avr" ,i,
			#print unicode(temp)
			i=i+1
		else: 
			if temp['name'] != '' and '???' not in temp['name'] :
				code.append(temp)
				#if len(temp['name'])>namelen:
				#	namelen=len(temp['name'])
		
	return code

def parseocd():
	global namelen
	status="test"
	p = subprocess.Popen("ls tcl/target",shell=True ,stdout=subprocess.PIPE)
	template={"processor":"","name":"","vendor":"","program":"openocd"}
	codeoc=[]
	i=0
	while status!='done':
		temp=template
		buf=p.stdout.readline()
		buf,ignored,ignored=buf.partition(".cfg")
		buf,ignored,ignored=buf.partition(".tcl")
		temp['processor']=buf
		temp['name']=buf
		line=json.dumps(temp)
		temp=json.loads(line)
		if len(temp['name'])>namelen:
			namelen=len(temp['name'])

		if unicode("u'"+temp['name']+"', ") in unicode(code):
			print "ocd" ,i
			print temp
			i=i+1
		else: 
			if temp['name'] != '':
				code.append(temp)			
		if buf == '' and p.poll()!= None:
			status='done'
	

	p = subprocess.Popen("ls tcl/board",shell=True ,stdout=subprocess.PIPE)

	codeoc=[]
	i=0
	status="test"
	while status!='done':
		temp=template
		buf=p.stdout.readline()
		buf,ignored,ignored=buf.partition(".cfg")
		buf,ignored,ignored=buf.partition(".tcl")
		temp['processor']=buf
		temp['name']=buf
		line=json.dumps(temp)
		temp=json.loads(line)	
		if len(temp['name'])>namelen:
			namelen=len(temp['name'])
		if unicode("u'"+temp['name']+"',") in unicode(code):
			#print "board" ,i
			#print unicode("u'"+temp['name']+"', ")
			#print temp
			i=i+1
		else: 
			if temp['name'] != '':
				code.append(temp)			
		if buf == '' and p.poll()!= None:
			status='done'
	

			

		
	return code

def makephp():
	i=1
	help=True
	with open('./processor.php','w') as w:
	 with open('./avrdude.rc','w') as a:
	  with open('./openocd.rc','w') as o:
		w.write("<?php\n\n")
		w.write("$processors = array(")
		code.sort(key=lambda name: name)
		while help==True:
			try:
				
				tempid=code[i]['processor']
				tempname=code[i]['name']
				tempvendor=code[i]['vendor']
				tempprogram=code[i]['program']

				if code[i]['program'] == 'avrdude':
					a.write(tempid+'\n')

				if code[i]['program'] == 'openocd':
					o.write(tempid+'\n')
				vendorspace=""
				namespace=""
				y=0
				x=0
				if len(tempname) < namelen:
					#print namelen,len(tempname)
					y=int(namelen-int(len(tempname)))
					
					while x < y:
						
						namespace=namespace+"&nbsp;"
						x=x+1
				#print "namelen",y," == ",len(namespace)/6
				y=0
				x=0
				if len(tempvendor) < vendorlen:
					#print vendorlen,len(tempvendor)
					y=vendorlen-len(tempvendor)
					
					while x < y:
					
						vendorspace=vendorspace+"&nbsp;"
						x=x+1
				#print "vendorlen",y," == ",len(vendorspace)/6
				w.write("'"+unicode(tempvendor)+vendorspace+" "+unicode(tempname)+namespace+" "+unicode(tempprogram)+"'=>'"+unicode(tempid)+"',")
				i=i+1
			except Exception as e: 
				print "error"
				
				print e,i
    				
				
				help=False
				w.write(")\n?>")
				
code =readfile()
code = parseavr()
code=parseocd()
#print code
makephp()
print ""
print ""
print ""
print ""
