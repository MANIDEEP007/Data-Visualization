#This is used for educational Purpose
import urllib as url
from bs4 import BeautifulSoup as bs
import sys
import os
from selenium import webdriver
import datetime
import csv
from PyQt5.QtWidgets import QApplication as QApp
from PyQt5.QtWidgets import QWidget as QWid
from PyQt5.QtGui import QIcon as Qico
from PyQt5.QtWidgets import QStatusBar as QStat
from PyQt5.QtWidgets import QMainWindow as QMWin
from PyQt5.QtWidgets import QLabel as QLbl
from PyQt5.QtWidgets import QPushButton as QBtn
from PyQt5.QtWidgets import QHBoxLayout as HBox
from PyQt5.QtWidgets import QComboBox as CBox 
from PyQt5.QtWidgets import QVBoxLayout as VBox
from PyQt5.QtWidgets import QGridLayout as Grid
from PyQt5.QtCore import QRect as Rect
from PyQt5.QtCore import Qt
#Scraping TutorialPoint
if(not os.path.exists("COURSES")):
	os.mkdir("COURSES")
page_url = "https://www.tutorialspoint.com/tutorialslibrary.htm"
page = url.request.urlopen(page_url)
parser = bs(page,'html.parser')
courses = parser.find_all("ul",attrs={'class':'menu'});
headings=[]
for i in parser.find("div",attrs={'class':'featured-boxes'}).find_all("h4"):
	headings.append(i.text)
file_index =0
for looper in range(0,len(courses)):
	list_courses = []
	list_urls =[]
	li = courses[looper].findChildren("li",recursive = False)
	for courses[looper] in li:
		a = courses[looper].find("a")
		if(a['href'].startswith("/")):
			list_urls.append("https://www.tutorialspoint.com"+a['href'])
		else:
			list_urls.append("https://www.tutorialspoint.com/"+a['href'])
		if courses[looper].text.strip()[0]!='0':
			list_courses.append(courses[looper].text.strip())
	index = 0
	file_name = "COURSES/"+headings[looper]+".csv"
	excel = open(file_name,"a")
	object_write = csv.writer(excel)
	for i in range(0,len(list_courses)):
		index += 1
		object_write.writerow([index,list_courses[i],list_urls[i]])
#End of Scraping TutorialPoint
#Getting Categories
list_files = []
for root,dirs,files in os.walk("COURSES"):
	for file_obj in files:
		list_files.append(file_obj[:-4])
#End of Getting Categories
class App(QWid):
	def __init__(self):
		super().__init__()
		self.title = "Tutorial Point Scrapper"
		self.showMaximized()
		self.initUI()
	def initUI(self):
		self.setWindowIcon(Qico('pythonlogo.png'))
		self.setWindowTitle(self.title)
		self.SetWidgets()
		self.show()
	def Selector(self,index):
		self.scbox.clear()
		self.scbox.addItem("--Select--")
		if self.cbox.currentText() != "--Select--":
			file_name = "COURSES/"+self.cbox.currentText()+".csv"
			csv_file = open(file_name)
			csv_reader = csv.reader(csv_file,delimiter =',')
			for i in csv_reader:
				self.scbox.addItem(i[1]) 
	def Clicked(self):
		if self.cbox.currentText() != "--Select--":
			file_name = "COURSES/"+self.cbox.currentText()+".csv"
			csv_file = open(file_name)
			csv_reader = csv.reader(csv_file,delimiter =',')
			if self.scbox.currentText() != "--Select--":		
				for i in csv_reader:
					if(i[1] == self.scbox.currentText()):
						url_open = i[2]
						break
				driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
				driver.get (url_open) 
	def SetWidgets(self):
		#Grid Layout
		layout = Grid()
		layout.setColumnStretch(1,9)
		layout.setColumnStretch(2,9)
		layout.setColumnStretch(3,9)
		layout.setColumnStretch(4,9)
		layout.setColumnStretch(5,9)
		layout.setColumnStretch(6,9)
		layout.setColumnStretch(7,9)
		layout.setColumnStretch(8,9)
		layout.setColumnStretch(9,9)
		layout.setRowStretch(0,3)
		layout.setRowStretch(1,11)
		layout.setRowStretch(2,11)
		layout.setRowStretch(3,11)
		layout.setRowStretch(4,11)
		layout.setRowStretch(5,11)
		layout.setRowStretch(5,11)
		layout.setRowStretch(6,11)
		layout.setRowStretch(7,11)
		layout.setRowStretch(8,11)
		layout.setRowStretch(9,11)
		layout.setRowStretch(10,11)
		layout.setRowStretch(11,11)
		#End of Grid Layout
		self.main = QLbl("Tutorial Point Library Searcher")
		self.main.setStyleSheet('''QLabel{font-size:30px;font-weight:bold;text-align:center;}''')
		layout.addWidget(self.main,0,4,1,4)
		#Category Widget		
		self.cbox = CBox()
		self.cbox.setGeometry(80,10,60,10)
		self.cbox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.cbox.view().setHorizontalScrollBarPolicy (Qt.ScrollBarAlwaysOff)
		self.cbox.view().setAutoScroll(True)
		self.cbox.addItem("--Select--")
		for i in list_files:
			self.cbox.addItem(i)
		self.category = QLbl("Category")
		layout.addWidget(self.category,2,4,1,1)
		layout.addWidget(self.cbox,2,5,1,1)
		self.cbox.currentIndexChanged.connect(self.Selector)
		#End of Category Widget
		#Sub Category Widget		
		self.scbox = CBox()
		#self.scbox.setGeometry(80,10,60,10)
		self.scbox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.scbox.view().setHorizontalScrollBarPolicy (Qt.ScrollBarAlwaysOff)
		self.scbox.view().setAutoScroll(True)
		self.subcategory = QLbl("Sub Category")
		self.scbox.addItem("--Select--")
		layout.addWidget(self.subcategory,4,4,1,1)
		layout.addWidget(self.scbox,4,5,1,1)
		#End of Sub Category Widget
		#StatusBar Widget		
		self.statusBar = QStat()
		self.statusBar.showMessage(datetime.date.today().strftime("%d %b %Y"))
		self.statusBar.setStyleSheet('''QStatusBar{padding-left:50%;background-color:blue;color:white;font-weight:16px;text-align:center;}''')
		layout.addWidget(self.statusBar,11,0,1,10)
		#End of StatusBar Widget
		#Go Button
		self.go = QBtn("Go")
		layout.addWidget(self.go,6,5,1,1)
		self.go.setStyleSheet('''QPushButton{color:white;background-color:green;}''')
		self.go.clicked.connect(self.Clicked)
		#End of Go Button
		self.setLayout(layout)
app_obj = QApp(sys.argv)
execute = App()
sys.exit(app_obj.exec_())
