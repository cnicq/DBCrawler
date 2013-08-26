#coding=utf-8
import csv
import os
import sys
import os.path
import pymongo
import logging
import time
from Data_Manager import MetaData_Insert,TargetData_Insert
from DBCrawler.datatypes.DBTypes import IndicatorData, MetaData, TargetData, AreaData,TargetData

def Sina_CSV_Parser():
	#for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\sina'):
	for dirpath, dirnames, filenames in os.walk('C:\\Git\\DBCrawler\\DBCrawler\\media\\indicator'):
		for filename in filenames:
			if os.path.splitext(filename)[1] == '.csv':
				filepath = os.path.join(dirpath, filename)
				csvlines = csv.reader(open(filepath, 'r'))
				lines = {}
				IndicatorTypeCode = ""
				n = 0
				HasArea = False
				HasSubType = False
				StarIndex = 3
				HasRowTarget = False
				MainIndicatorName = u''
				SubIndicatorName = u''
				print filename
				# 1.record lines and infos
				for line in csvlines:
					lines[n] = line;
					n += 1
				for i in range(0, len(lines)):
					for j in range(0, len(lines[i])):
						lines[i][j] = unicode(lines[i][j].replace(' ',''),('gbk'))

				# 2.if second col of third row can not canvert to float, ot check if it's area
				if u'地区' in lines[2][1]:
					HasArea = True
				if lines[3][0] == '':
					HasSubType = True
					StarIndex = 4

				# 3. src target
				MainIndicatorName = ''
				IndicatorNote = ''
				if lines[0][0] != '':
					MainIndicatorName = lines[0][0].split('_')[2]
				else:
					MainIndicatorName = lines[0][1]
				IndicatorNote = lines[0][2];
				SrcTargetName = ''
				if lines[0][3] != '':
					SrcTargetName = lines[0][3]
				else:
					SrcTargetName = u'互联网'
				TheSrcTargetData = TargetData_Insert(SrcTargetName, 'organization', con);

				# 4.iterator the rows	
				for i in range(StarIndex, len(lines)):

					TargetName1 = u''
					TargetName2 = u''
					AreaName = u'中国'
					fValue = 0

					HasRowTarget = False
					for j in range(0, len(lines[i])):
						if j == 0:
							continue;
						if j == 1 and HasArea == True:
							AreaName = lines[i][j]
							if AreaName == u'':
								AreaName = u'中国'
							elif AreaName == u'全国' or AreaName == u'合计':
								AreaName = u'中国'
							continue;
						if j == 1 and HasArea == False:
							try:
								fValue = float(lines[i][1])
							except:
								HasRowTarget = True
								continue;
						strValue = lines[i][j].replace(' ','')
						if strValue == '':
							continue;

						fValue = float(strValue)
						if HasSubType == True and lines[StarIndex-2][j] != "":
							SubIndicatorName = lines[StarIndex-2][j]
						if HasRowTarget == True:
							TargetName1 = lines[i][1]
							TargetName2 = lines[StarIndex-1][j]
						else:
							TargetName2 = lines[StarIndex-1][j]

						IndicatorName = MainIndicatorName
						if SubIndicatorName != u'':
							IndicatorName = MainIndicatorName + u'(' + SubIndicatorName + u')'
						MetaData_Insert(con, lines[i][0], fValue, IndicatorName, IndicatorNote,
						 	AreaName, '','', TargetName1, TargetName2, 
						 	TheSrcTargetData['NameLoc']['Chinese'], TheSrcTargetData['Type'])

logger = logging.getLogger() 
file = logging.FileHandler("Sina_XLS_Parser.log")
logger.addHandler(file)

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		Sina_CSV_Parser()