from django.shortcuts import render
from .models import scrapped
import requests
from bs4 import BeautifulSoup
import io
import codecs
from selenium import webdriver
import time


# Create your views here.
URL=""
class1=""
page_source = ""
driver = ""
Page=""
soup=""
Yaxis=[]
Xaxis=[]
Xaxis1=[]
Xaxis2=[]
def index(request):
	return render(request, 'index.html')

def WebDriverCall(request):
	global page_source
	global driver
	global URL, Page
	URL=request.POST["url"]
	Page=request.POST["PageType"]

	if(Page=="Static"):
		return render(request, 'result.html',{'url':URL})
	if(Page=="Dynamic"):
		try:
			driver = webdriver.Chrome(r"C:\Users\Admin\projects\webScrapper\WScrapper\chromedriver")
			driver.get(URL)
			query=r"$(document).ready(function(){$('*').click(function(event){var myClass = $(this).attr('class');alert(myClass);event.preventDefault();event.stopImmediatePropagation();return false;});});function refreshData(){x=1;$('*').click(function(event){var myClass = $(this).attr('class');alert(myClass);event.preventDefault();event.stopImmediatePropagation();return false;});setTimeout(refreshData, x*1000);}refreshData();"
			driver.execute_script(query)
		except:
			temp="Error Occured! Please try again."
		return render(request, 'resultDynamic.html',{'url':URL})

def outcome(request):
	global driver
	global class1
	global page_source
	global URL,Yaxis,Xaxis,	Xaxis1,	Xaxis2
	global soup
	bhk1=0
	bhk2=0
	bhk3=0
	bhk4=0
	bhk5=0
	bhk1p=0
	bhk2p=0
	bhk3p=0
	bhk4p=0
	bhk5p=0
	b1h=0
	b2h=0
	b3h=0
	b4h=0
	b5h=0
	b1l=0
	b2l=0
	b3l=0
	b4l=0
	b5l=0
	lowestPCount1=0
	lowestPCount2=0
	lowestPCount3=0
	lowestPCount4=0
	lowestPCount5=0

	if(Page=="Static"):
		headers ={ "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
		page = requests.get(URL, headers=headers)
		soup = BeautifulSoup(page.text,'lxml')

	else:
		page_source = driver.page_source
		soup = BeautifulSoup(page_source,'lxml')
	class1=[]
	class1=request.POST["class"].split(",")
	tags=['div','span','p','h1','h2','h3','h4','h5','h6','a']
	for tag in tags:
		str1= tag+"[class*="+str(class1[0])+"]"
		str2= tag+"[class*="+str(class1[1])+"]"
		temp=""
		a=""
		for i,j in  zip(soup.select(str1),soup.select(str2)):
			temp=j.get_text()
			temp=temp.replace("\n"," ")
			temp=temp.replace("  ","")
			temp=temp.replace("\t","")
			temp=temp.replace(","," ")
			d=temp.split(" ")
			temp=i.get_text()+", "+temp
			a=a+"\n"+temp
			k=i.get_text().split(" ")

			if(k[1]=="Cr"):
				k[0]=str(float(k[0])*100)

			if(d[1] == '1'):
				bhk1+=1
				if(float(k[0])>float(b1h)):
					b1h=float(k[0])

				bhk1p=bhk1p+float(k[0])
				if(lowestPCount1==0):
					b1l=float(k[0])
					lowestPCount1=1

				if(float(b1l)>float(k[0])):
					b1l=float(k[0])

			elif(d[1] == '2'):
				bhk2+=1
				if(float(k[0])>float(b2h)):
					b2h=float(k[0])
				bhk2p=bhk2p+float(k[0])

				if(lowestPCount2==0):
					b2l=float(k[0])
					lowestPCount2=1

				if(float(b2l)>float(k[0])):
					b2l=float(k[0])

			elif(d[1] == '3'):
				bhk3+=1
				if(float(k[0])>float(b3h)):
					b3h=float(k[0])
				bhk3p=bhk3p+float(k[0])
				if(lowestPCount3==0):
					b3l=float(k[0])
					lowestPCount3=1

				if(float(b3l)>float(k[0])):
					b3l=float(k[0])

			elif(d[1] == '4'):
				bhk4+=1	
				if(float(k[0])>float(b4h)):
					b4h=float(k[0])
				bhk4p=bhk4p+float(k[0])
				if(lowestPCount4==0):
					b4l=float(k[0])
					lowestPCount4=1

				if(float(b4l)>float(k[0])):
					b4l=float(k[0])

			elif(d[1] == '5'):
				bhk5+=1
				if(float(k[0])>float(b5h)):
					b5h=float(k[0])
				bhk5p=bhk5p+float(k[0])
				if(lowestPCount5==0):
					b5l=float(k[0])
					lowestPCount5=1

				if(float(b5l)>float(k[0])):
					b5l=float(k[0])
			
		if(a !=""):
			break
	if(float(bhk1)!=0):
		b1=float(bhk1p)/float(bhk1)
	if(float(bhk2)!=0):
		b2=float(bhk2p)/float(bhk2)
	if(float(bhk3)!=0):
		b3=float(bhk3p)/float(bhk3)
	if(float(bhk4)!=0):
		b4=float(bhk4p)/float(bhk4)
	Yaxis=["1BHK", "2BHK", "3BHK", "4BHK"]
	Xaxis=[b1,b2,b3,b4]
	Xaxis1=[b1h,b2h,b3h,b4h]
	Xaxis2=[b1l,b2l,b3l,b4l]
	return render(request, 'output.html',{'rest':a,'Yaxis':Yaxis,'Xaxis':Xaxis,'Xaxis1':Xaxis1,'Xaxis2':Xaxis2})

def downloadCSV(request):
	global driver
	global class1
	global soup
	global URL,Yaxis,Xaxis,	Xaxis1,	Xaxis2
	global page_source
	global URL
	filename="ScrapeSilver.csv"
	#f=open(filename,"w")
	f = codecs.open(filename, "w", "utf-8")
	tags=['div','span','p','h1','h2','h3','h4','h5','h6','a']
	for tag in tags:
		str1= tag+"[class*="+str(class1[0])+"]"
		str2= tag+"[class*="+str(class1[1])+"]"
		temp=""
		a=""
		for i,j in  zip(soup.select(str1),soup.select(str2)):
			temp=j.get_text()
			temp=temp.replace("\n"," ")
			temp=temp.replace("  ","")
			temp=temp.replace("\t","")
			temp=temp.replace(","," ")
			temp=i.get_text()+", "+temp
			a=a+"\n"+temp
			
			f.write(str(temp)+"\n")
	
		if(a !=""):
			break
	f.close()
	done="Downloaded File Successfully"
	return render(request, 'output.html',{'rest':a,'done':done,'Yaxis':Yaxis,'Xaxis':Xaxis,'Xaxis1':Xaxis1,'Xaxis2':Xaxis2})

def FindClassStatic(request):
	global URL
	global driver
	option = webdriver.ChromeOptions()
	option.add_argument('headless')
	driver = webdriver.Chrome(r"C:\Users\Admin\projects\webScrapper\WScrapper\chromedriver",options=option)
	#driver = webdriver.Chrome(r"C:\Users\Admin\projects\webScrapper\WScrapper\chromedriver")
	driver.get(URL)
	query=r"$(document).ready(function(){$('*').click(function(event){var myClass = $(this).attr('class');alert(myClass);event.preventDefault();event.stopImmediatePropagation();return false;});});function refreshData(){x=1;$('*').click(function(event){var myClass = $(this).attr('class');alert(myClass);event.preventDefault();event.stopImmediatePropagation();return false;});setTimeout(refreshData, x*1000);}refreshData();"
	q1=r"var script = document.createElement('script');script.type='text/javascript';script.src ='https://code.jquery.com/jquery-3.4.1.js';document.body.appendChild(script);var script = document.createElement('script');script.type='text/javascript';script.src ='https://code.jquery.com/jquery-3.4.1.js';document.head.appendChild(script);"
	driver.execute_script(q1)
	page_source = driver.page_source	
	with io.open("temp.html", "w", encoding="utf-8") as f:
		f.write(str(page_source))
	f.close()
	f=open("temp.html","a")
	f.write(str("<script>$(document).ready(function(){$('*').click(function(event){var myClass = $(this).attr('class');alert(myClass);event.preventDefault();event.stopImmediatePropagation();return false;});});function refreshData(){x=1;$('*').click(function(event){var myClass = $(this).attr('class');alert(myClass);event.preventDefault();event.stopImmediatePropagation();return false;});setTimeout(refreshData, x*1000);}refreshData();</script>"))
	f.close()
	URL1=r"C:\Users\Admin\Documents\Collegebookspdf\Sem-4\ADPROJECT\webScrapper\temp.html"
	driver = webdriver.Chrome(r"C:\Users\Admin\projects\webScrapper\WScrapper\chromedriver")
	driver.get(URL1)
	driver.execute_script(query)
	return render(request, 'result.html',{'url':URL})