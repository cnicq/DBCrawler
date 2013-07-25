#coding=utf-8
import csv
import os
import sys
import os.path
import pymongo
import logging
#from DBCrawler.datatypes.DBTypes import IndicatorData, MetaData, TargetData, AreaData
#from DBCrawler.datatypes.Types import IndicatorType,MetaData,Target

class IndicatorData:
	Keywords = []
	NameLoc = {}
	SrcTarget = ""
	Note = ""
	OutURL = ""

	def ToMap(self):
		DataMap = {}
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if len(self.Keywords) > 0:
			DataMap['Keywords'] = self.Keywords;
		if self.SrcTarget != '':
			DataMap['SrcTarget'] = self.SrcTarget;
		if self.Note != '':
			DataMap['Note'] = self.Note;
		if self.OutURL != '':
			DataMap['OutURL'] = self.OutURL;

		return DataMap

class MetaData:
	AreaID = ""
	Target1ID = ""
	Target2ID = ""
	Period = ""
	Datas = []

	def ToMap():
		DataMap = {}
		if AreaID != '':
			DataMap['AreaID'] = AreaID;
		if Target1ID != '':
			DataMap['Target1ID'] = Target1ID;
		if Target2ID != '':
			DataMap['Target2ID'] = Target2ID;
		if Period != '':
			DataMap['Period'] = Period;
		if len(Datas) > 0:
			DataMap['Datas'] = Datas;

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
		if self.BelongArea != '':
			DataMap['BelongArea'] = self.BelongArea;
		if self.MapName != '':
			DataMap['MapName'] = self.MapName;
		if self.MapPos != '':
			DataMap['MapPos'] = self.MapPos;

		return DataMap


class TargetData:
	NameLoc = {}
	Type = ""
	Note = ""
	URLs = "[]"

	def ToMap():
		DataMap = {}
		if URLs != '':
			DataMap['URLs'] = URLs;
		if len(NameLoc) > 0:
			DataMap['NameLoc'] = NameLoc;
		if MapPos != '':
			DataMap['Type'] = Type;
		if Note != '':
			DataMap['Note'] = Note;
		return DataMap

class CatalogData:
	NameLoc = []
	ParentName = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['ParentName'] = ParentName;
		return DataMap



def Add_MetaData(i, j, dValue, fValue, IndicatorName, AreaName, TargetName1, TargetName2, SrcTarget):
	#dValue = dValue.replace(' ','').encode('utf8')
	IndicatorName = IndicatorName.replace(' ','').decode('gbk')
	#AreaName = AreaName.replace(' ','').encode('utf8')
	#TargetName1 = TargetName1.replace(' ','').encode('utf8')
	#TargetName2 = TargetName2.replace(' ','').encode('utf8')
	SrcTarget = SrcTarget.replace(' ','')
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
		TheIndicatorData.SrcTarget = SrcTarget
		con.DBStore.IndicatorData.insert(TheIndicatorData.ToMap())
	TheIndicatorData = con.DBStore.IndicatorData.find_one({"NameLoc":{"Chinese":IndicatorName}})
	if TheIndicatorData is None:
		print 'Error : Insert indicator data to mongodb failed.'
		return

	return;
	#check if has area by area name
	TheAreaData = con.DBStore.AreaData.find_one({"NameLoc":{"Chinese":AreaName}})
	if TheAreaData is None:
		TheAreaData = AreaData()
		TheAreaData.NameLoc = '[Chinese:' + AreaName + ']'
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
			TheTargetData1.NameLoc = '[Chinese:' + AreaName + ']'
			TheTargetData1.Type = 'Indicator'
			con.DBStore.AreaData.insert(TheTargetData1.ToMap())
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
			TheTargetData2.NameLoc = '[Chinese:' + AreaName + ']'
			TheTargetData2.Type = 'Indicator'
			con.DBStore.AreaData.insert(TheTargetData2.ToMap())
		TheTargetData2 = con.DBStore.TargetData.find_one({"NameLoc":{"Chinese":TargetName2}})
		if TheTargetData2 is None:
			print 'Error : Insert target data to mongodb failed.'
			return

	# set period type by date format
	dValues = len(dValue.split('.'))
	Period = 'year'
	if dValues == 1:
		Period = 'year'
	elif dValues == 2:
		Period = 'month'
	elif dValues == 3:
		period = 'day'
	else:
		print 'Error : The period data has error.'
		return

	MetaDataCollectionName = 'MetaData_' + TheIndicatorData._id;
	TheMetaData = con.DBStore.MetaDataCollectionName.find_one(
		{"AreaID":TheAreaData._id},
		{"Target1ID":TheTargetData1._id},
		{"Target2ID":TheTargetData2._id},
		{"Period":period},
		{"Datas":{"Date":dValue}})
	if TheMetaData is None:
		TheMetaData = MetaData()
		TheMetaData.AreaID = TheAreaData._id;
		if TheTargetData1 != None:
			TheMetaData.Target1ID = TheTargetData1._id;
		if TheTargetData2 != None:
			TheMetaData.Target2ID = TheTargetData2._id;
		TheMetaData.Period = period
		TheMetaData.Datas = []
		TheMetaData.Datas[0] = {"Datas":{"Date":dValue,"Value":fValue,"UpdateDate":strftime()}}
		# insert new
		con.DBStore.MetaDataCollectionName.insert(TheMetaData)
	else:
		#update
		con.DBStore.MetaDataCollectionName.update({"_id":TheMetaData._id}, 
			{'$push':{"Datas":{"Date":dValue,"Value":fValue,"UpdateDate":strftime()}}})

	
def Sina_CSV_Parser():
	for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\sina'):
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
				MainIndicatorName = ""
				SubIndicatorName = ""

				# 1.record lines and infos
				for line in csvlines:
					lines[n] = line;
					n += 1

				# 2.if second col of third row can not canvert to float, ot check if it's area
				if u'地区' in lines[2][1].replace(' ','').decode('gbk'):
					HasArea = True
				if lines[3][0] == '':
					HasSubType = True
					StarIndex = 4
				print filename
				# 3.iterator the rows	
				MainIndicatorName = lines[0][0].split('_')[2]

				for i in range(StarIndex, len(lines)):
					TargetName1 = ""
					TargetName2 = ""
					AreaName = u'中国'
					fValue = 0
					HasRowTarget = False
					print lines[i]
					for j in range(0, len(lines[i])):
						if j == 0:
							continue;
						if j == 1 and HasArea == True:
							AreaName = lines[i][1]
							if AreaName == u'全国' or AreaName == u'合计':
								AreaName = u'中国'
							if AreaName == '':
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
							continue;
						else:
							TargetName1 = lines[StarIndex-1][j]
						IndicatorName = MainIndicatorName
						if SubIndicatorName != '':
							IndicatorName = MainIndicatorName + '(' + SubIndicatorName + ')'
						Add_MetaData(i,j,lines[i][0], fValue, IndicatorName, AreaName, TargetName1, TargetName2, u'新浪数据')

logger = logging.getLogger() 
file = logging.FileHandler("Sina_XLS_Parser.log")
logger.addHandler(file)

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		Sina_CSV_Parser()