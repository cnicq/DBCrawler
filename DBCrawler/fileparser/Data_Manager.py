#coding=utf-8
import csv
import os
import sys
import os.path
import pymongo
import logging
import time

from DBCrawler.datatypes.DBTypes import IndicatorData, CombinedData

def CombinedData_Creator(IndicatorData, con):
	if IndicatorData != None and IndicatorData['CombinedDataID'] == None:
		TheCombinedData = CombinedData()
		TheCombinedData.NameLoc['Chinese'] = IndicatorData['NameLoc']['Chinese']
		Condition = {};
		Condition['IndicatorID'] = IndicatorData['_id']
		TheCombinedData.Conditions.append(Condition);
		if 'Note' in IndicatorData:
			TheCombinedData.Note = IndicatorData['Note'];
		return con.DBStore.CombinedData.insert(TheCombinedData.ToMap());
