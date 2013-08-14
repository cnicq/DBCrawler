#coding=utf-8
import csv
import os
import sys
import os.path
import pymongo
import logging
import time
import pymongo

from DBCrawler.datatypes.DBTypes import IndicatorData, CombinedData,AreaData
insert_counter = 0

def CombinedData_Creator(IndicatorData, con):
	if IndicatorData != None and ("CombinedDataID" not in IndicatorData or IndicatorData['CombinedDataID'] == None):
		TheCombinedData = CombinedData()
		TheCombinedData.NameLoc['Chinese'] = IndicatorData['NameLoc']['Chinese']
		Condition = {};
		Condition['IndicatorID'] = IndicatorData['_id']
		TheCombinedData.Conditions.append(Condition);
		if 'NoteLoc' in IndicatorData:
			TheCombinedData.NoteLoc = IndicatorData['NoteLoc'];
		TheCombinedData.UpdateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
		return con.DBStore.CombinedData.insert(TheCombinedData.ToMap());
	return "NotChanged"

def IndicatorData_CreateDefaultCombinedData():
	TheIndicatorDatas = con.DBStore.IndicatorData.find()
	for IndicatorData in TheIndicatorDatas:
		if "CombinedDataID" in IndicatorData and IndicatorData['CombinedDataID'] != None:
			if(con.DBStore.CombinedData.find_one({"_id" : IndicatorData['CombinedDataID']}) == None):
				IndicatorData['CombinedDataID'] = None;
		CombinedDataID = CombinedData_Creator(IndicatorData, con);
		if CombinedDataID == "NotChanged":
			continue;
		con.DBStore.IndicatorData.update({"_id":IndicatorData['_id']},{'$set' : {'CombinedDataID':CombinedDataID}})
		print CombinedDataID;

def AreaData_Insert(ChineseName, EnglishName, SC2, SC3, NumberCode, AreaType, BelongAreaID, MapName, MapPos, con):
	TheAreaData = con.DBStore.AreaData.find_one({"NameLoc":{"Chinese":ChineseName}})
	if TheAreaData is None:
		TheAreaData = AreaData()
		TheAreaData.NameLoc['Chinese'] = ChineseName
		TheAreaData.NameLoc['English'] = EnglishName
		TheAreaData.SC2 = SC2
		TheAreaData.SC3 = SC3
		TheAreaData.NumberCode = NumberCode
		TheAreaData.AreaType = AreaType
		TheAreaData.BelongAreaID = BelongAreaID
		TheAreaData.MapName = MapName
		TheAreaData.MapPos = MapPos
		TheAreaData = con.DBStore.AreaData.insert(TheAreaData.ToMap())
	return TheAreaData;


def MetaData_Insert(dValue, fValue, IndicatorName, AreaName, TargetName1, TargetName2, SrcTarget, con):
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

	# add default combined data if needed
	if TheIndicatorData['CombinedDataID'] == None:
		CombinedDataID = CombinedData_Creator(TheIndicatorData, con);
		print CombinedDataID;
		if CombinedDataID != None:
			con.DBStore.IndicatorData.update({"_id":TheIndicatorData['_id']},{'$set' : {'CombinedDataID':CombinedDataID}})

	#check if has area by area name
	TheAreaData = AreaData_Insert('', AreaName)
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

	

def Manager_Cmd():
	print "Manager Command List : "
	print "1. Create default combined data for all indicator data"
	index = int(raw_input("please input:"))
	if (index == 1):
		IndicatorData_CreateDefaultCombinedData();
'''
con = pymongo.Connection('localhost', 27017)
if con:
	db = con.DBStore
	if db:
		Manager_Cmd();
'''