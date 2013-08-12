#coding=utf-8
import csv
import os
import sys
import os.path
import pymongo
import logging
import time
#from DBCrawler.datatypes.DBTypes import IndicatorData, MetaData, TargetData, AreaData
#from DBCrawler.datatypes.Types import IndicatorType,MetaData,Target

class IndicatorData:
	Keywords = []
	NameLoc = {}
	SrcTargetID = None
	Note = ""
	OutURL = ""

	def __init__(self):
		self.Keywords = []
		self.NameLoc = {}
		self.SrcTargetID = None
		self.Note = ""
		self.OutURL = ""

	def ToMap(self):
		DataMap = {}
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if len(self.Keywords) > 0:
			DataMap['Keywords'] = self.Keywords;
		if self.SrcTargetID != None:
			DataMap['SrcTargetID'] = self.SrcTargetID;
		if self.Note != '':
			DataMap['Note'] = self.Note;
		if self.OutURL != '':
			DataMap['OutURL'] = self.OutURL;

		return DataMap

class MetaData:
	AreaID = ""
	Target1ID = None
	Target2ID = None
	Period = ""
	Datas = []

	def __init__(self):
		self.AreaID = ""
		self.Target1ID = None
		self.Target2ID = None
		self.Period = ""
		self.Datas = []

	def ToMap(self):
		DataMap = {}
		if self.AreaID != None:
			DataMap['AreaID'] = self.AreaID;
		if self.Target1ID != None:
			DataMap['Target1ID'] = self.Target1ID;
		if self.Target2ID != None:
			DataMap['Target2ID'] = self.Target2ID;
		if self.Period != '':
			DataMap['Period'] = self.Period;
		if len(self.Datas) > 0:
			DataMap['Datas'] = self.Datas;

		return DataMap

class AreaData:
	NameLoc = {}
	SC2 = ""
	SC3 = ""
	NC = ""
	NameFull = ""
	AreaType = ""
	BelongAreaID = ""
	MapName = ""
	MapPos = ""

	def __init__(self):
		self.NameLoc = {}
		self.SC2 = ""
		self.SC3 = ""
		self.NC = ""
		self.NameFull = ""
		self.AreaType = ""
		self.BelongAreaID = ""
		self.MapName = ""
		self.MapPos = ""
	def ToMap(self):
		DataMap = {}
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if self.SC2 != '':
			DataMap['SC2'] = self.SC2;
		if self.SC3 != '':
			DataMap['SC3'] = self.SC3;
		if self.NC != '':
			DataMap['NC'] = self.NC;
		if self.NameFull != '':
			DataMap['NameFull'] = self.NameFull;
		if self.AreaType != '':
			DataMap['AreaType'] = self.AreaType;
		if self.BelongAreaID != '':
			DataMap['BelongArea'] = self.BelongAreaID;
		if self.MapName != '':
			DataMap['MapName'] = self.MapName;
		if self.MapPos != '':
			DataMap['MapPos'] = self.MapPos;

		return DataMap


class TargetData:
	NameLoc = {}
	Type = ""
	Note = ""
	URLs = []

	def __init__(self):
		self.NameLoc = {}
		self.Type = ""
		self.Note = ""
		self.URLs = []

	def ToMap(self):
		DataMap = {}
		if len(self.URLs) > 0:
			DataMap['URLs'] = self.URLs;
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if self.Type != '':
			DataMap['Type'] = self.Type;
		if self.Note != '':
			DataMap['Note'] = self.Note;
		return DataMap

class CatalogData:
	NameLoc = {}
	ParentName = ""

	def ToMap(self):
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['ParentName'] = ParentName;
		return DataMap


insert_counter = 0
def Add_MetaData(i, j, dValue, fValue, IndicatorName, AreaName, TargetName1, TargetName2, SrcTarget):
	global insert_counter;
	insert_counter += 1
	print insert_counter
	dValue = dValue.encode('utf8')
	IndicatorName = IndicatorName.encode('utf8')
	AreaName = AreaName.encode('utf8')
	TargetName1 = TargetName1.encode('utf8')
	TargetName2 = TargetName2.encode('utf8')
	SrcTarget = SrcTarget.encode('utf8')
	if dValue == "":
		print 'Error : The data value is not set.'
		return

	#check src target
	TheSrcData = None
	if SrcTarget != '':
		TheSrcData = con.DBStore.TargetData.find_one({"NameLoc":{"Chinese":SrcTarget}})
		if TheSrcData is None:
			TheSrcData = TargetData()
			TheSrcData.NameLoc['Chinese'] = SrcTarget
			TheSrcData.Type = 'Company'
			con.DBStore.TargetData.insert(TheSrcData.ToMap())
		TheSrcData = con.DBStore.TargetData.find_one({"NameLoc":{"Chinese":SrcTarget}})
		if TheSrcData is None:
			print 'Error : Insert src target data to mongodb failed.'
			return

	#check if has indicator type by indicator name
	TheIndicatorData = con.DBStore.IndicatorData.find_one({"NameLoc":{"Chinese":IndicatorName}})
	if TheIndicatorData is None:
		TheIndicatorData = IndicatorData()
		TheIndicatorData.NameLoc['Chinese'] = IndicatorName
		TheIndicatorData.SrcTargetID = TheSrcData['_id']
		con.DBStore.IndicatorData.insert(TheIndicatorData.ToMap())
	TheIndicatorData = con.DBStore.IndicatorData.find_one({"NameLoc":{"Chinese":IndicatorName}})
	if TheIndicatorData is None:
		print 'Error : Insert indicator data to mongodb failed.'
		return

	#check if has area by area name
	TheAreaData = con.DBStore.AreaData.find_one({"NameLoc":{"Chinese":AreaName}})
	if TheAreaData is None:
		TheAreaData = AreaData()
		TheAreaData.NameLoc['Chinese'] = AreaName
		con.DBStore.AreaData.insert(TheAreaData.ToMap())
	TheAreaData = con.DBStore.AreaData.find_one({"NameLoc":{"Chinese":AreaName}})
	if TheAreaData is None:
		print 'Error : Insert area data to mongodb failed.'
		return

	
	#check if has target1 by target1 name
	TheTargetData1 = None
	if TargetName1 != '':
		TheTargetData1 = con.DBStore.TargetData.find_one({"NameLoc":{"Chinese":TargetName1}})
		if TheTargetData1 is None:
			TheTargetData1 = TargetData()
			TheTargetData1.NameLoc['Chinese'] = TargetName1
			TheTargetData1.Type = 'Indicator'
			con.DBStore.TargetData.insert(TheTargetData1.ToMap())
		TheTargetData1 = con.DBStore.TargetData.find_one({"NameLoc":{"Chinese":TargetName1}})
		if TheTargetData1 is None:
			print 'Error : Insert target data to mongodb failed.'
			return
	
	#check if has target2 by target2 name
	TheTargetData2 = None
	if TargetName2 != '':
		TheTargetData2 = con.DBStore.TargetData.find_one({"NameLoc":{"Chinese":TargetName2}})
		if TheTargetData2 is None:
			TheTargetData2 = TargetData()
			TheTargetData2.NameLoc['Chinese'] = TargetName2
			TheTargetData2.Type = 'Indicator'
			con.DBStore.TargetData.insert(TheTargetData2.ToMap())
		TheTargetData2 = con.DBStore.TargetData.find_one({"NameLoc":{"Chinese":TargetName2}})
		if TheTargetData2 is None:
			print 'Error : Insert target data to mongodb failed.'
			return

	# set period type by date format
	dValue = dValue.replace('/', '.');
	dValue = dValue.replace('-', '.');
	dValues = len(dValue.split('.'))

	Period = 'year'
	if dValues == 1:
		Period = 'year'
	elif dValues == 2:
		Period = 'month'
	elif dValues == 3:
		Period = 'day'
	else:
		print 'Error : The period data has error.'
		return
	
	MetaDataCollectionName = 'MetaData_' + str(TheIndicatorData['_id']);

	condistions = {}
	condistions['Period'] = Period
	if TheAreaData != None:
		condistions['AreaID'] = TheAreaData['_id']
	if TheTargetData1 != None:
		condistions['Target1ID'] = TheTargetData1['_id']
	if TheTargetData2 != None:
		condistions['Target2ID'] = TheTargetData2['_id']

	TheMetaData = con.DBStore[MetaDataCollectionName].find_one(condistions)
	strTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

	if TheMetaData is None:
		TheMetaData = MetaData()
		if TheAreaData != None:
			TheMetaData.AreaID = TheAreaData['_id'];
		if TheTargetData1 != None:
			TheMetaData.Target1ID = TheTargetData1['_id'];
		if TheTargetData2 != None:
			TheMetaData.Target2ID = TheTargetData2['_id'];
		TheMetaData.Period = Period
		# insert new
		TheMetaData.Datas.append({"Date":dValue,"Value":fValue,"UpdateDate":strTime})
		con.DBStore[MetaDataCollectionName].insert(TheMetaData.ToMap())
	else:
		#update
		# If the specific data has value, update it, else insert a new one
		con.DBStore[MetaDataCollectionName].update({"_id":TheMetaData['_id'] }, 
			{'$pull':{"Datas":{"Date":dValue}}})

		con.DBStore[MetaDataCollectionName].update({"_id":TheMetaData['_id']}, 
			{'$push':{"Datas":{"Date":dValue,"Value":fValue,"UpdateDate":strTime}}})

	
def Sina_CSV_Parser():
	#for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\sina'):
	for dirpath, dirnames, filenames in os.walk('C:\\Git\\DBCrawler\\DBCrawler\\media\\sina'):
	#for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\error'):
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
				# 3.iterator the rows	
				MainIndicatorName = lines[0][0].split('_')[2]

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
						Add_MetaData(i,j,lines[i][0], fValue, IndicatorName, AreaName, TargetName1, TargetName2, u'新浪数据')

logger = logging.getLogger() 
file = logging.FileHandler("Sina_XLS_Parser.log")
logger.addHandler(file)

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		Sina_CSV_Parser()