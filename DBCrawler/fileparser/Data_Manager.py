#coding=utf-8
import csv
import os
import sys
import os.path
import pymongo
import logging
import time
import pymongo

from DBCrawler.datatypes.DBTypes import IndicatorData, CombinedData

def CombinedData_Creator(IndicatorData, con):
	if IndicatorData != None and ("CombinedDataID" not in IndicatorData or IndicatorData['CombinedDataID'] == None):
		TheCombinedData = CombinedData()
		TheCombinedData.NameLoc['Chinese'] = IndicatorData['NameLoc']['Chinese']
		Condition = {};
		Condition['IndicatorID'] = IndicatorData['_id']
		TheCombinedData.Conditions.append(Condition);
		if 'Note' in IndicatorData:
			TheCombinedData.Note = IndicatorData['Note'];
		return con.DBStore.CombinedData.insert(TheCombinedData.ToMap());
	return "NotChanged"

def IndicatorData_Init():
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

def Manager_Cmd():
	print "Manager Command List : "
	print "1. Create default combined data for all indicator data"
	index = int(raw_input("please input:"))
	if (index == 1):
		IndicatorData_Init();

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		Manager_Cmd();