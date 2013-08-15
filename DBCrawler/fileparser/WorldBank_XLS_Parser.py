import xlrd
import os
import sys
import os.path
import pymongo
import logging
from Data_Manager import MetaData_Insert, IndicatorData_Insert, TargetData_Insert,AreaData_Insert
from DBCrawler.datatypes.DBTypes import IndicatorData, MetaData, TargetData, AreaData

def WorldBank_XLS_Parser():
	for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\worldbank'):
		for filename in filenames:
			if os.path.splitext(filename)[1] == '.xls':
				filepath = os.path.join(dirpath, filename)
				xlsfile = xlrd.open_workbook(filepath)
				sheet1 = xlsfile.sheet_by_name("Sheet1")
				sheet2 = xlsfile.sheet_by_name("Sheet2")

				# check to add the org target data
				SrcTargetData = TargetData_Insert(sheet2.row_values(1)[3], 'organization', con);
				if SrcTargetData == None:
					print "Error : SrcTargetData insert failed."
				# check to add the data indicator
				IndicatorData = IndicatorData_Insert(sheet2.row_values(1)[1], sheet2.row_values(1)[2], SrcTargetData['_id'], con);
				if IndicatorData == None:
					print "Error : IndicatorData insert failed."
					return;
				first_row = sheet1.row_values(0)
				for i in range(1, sheet1.nrows):
					AreaData = con.DBStore.AreaData.find_one({'SC3':sheet1.row_values(i)[1]});
					if AreaData == None:
						AreaData = AreaData_Insert(con, '', sheet1.row_values(i)[0], 'country', '', sheet1.row_values(i)[1], '', '')
					if AreaData == None:
						print "Error : AreaData insert failed."

					for j in range(2, sheet1.ncols):
						if sheet1.row_values(i)[j] != "":
							MetaData_Insert(con, first_row[j], sheet1.row_values(i)[j],
								IndicatorData['NameLoc']['Chinese'],
								IndicatorData['NoteLoc'],
								'',
								AreaData['NameLoc']['English'],
								AreaData['AreaType'],
								'',
								'',
								SrcTargetData['NameLoc']['Chinese'],
								SrcTargetData['Type'])

logger = logging.getLogger() 
file = logging.FileHandler("WorldBank_XLS_Parser.log")
logger.addHandler(file)

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		WorldBank_XLS_Parser()