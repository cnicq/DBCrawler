import xlrd
import os
import sys
import os.path
import pymongo
import logging
from Data_Manager import MetaData_Insert

from DBCrawler.datatypes.DBTypes import IndicatorData, MetaData, TargetData, AreaData

def WorldBank_XLS_Parser():
	return
	for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\worldbank'):
		for filename in filenames:
			if os.path.splitext(filename)[1] == '.xls':
				filepath = os.path.join(dirpath, filename)
				xlsfile = xlrd.open_workbook(filepath)
				sheet1 = xlsfile.sheet_by_name("Sheet1")
				sheet2 = xlsfile.sheet_by_name("Sheet2")

				#check the data indicator
				DataIndicators = con.DBStore.DataIndicators.find_one({"code":sheet2.row_values(1)[0]})
				code = "";
				if DataIndicators is None:
					Indicator = IndicatorType();
					Indicator.Name = sheet2.row_values(1)[0]
					Indicator.NameLoc = sheet2.row_values(1)[1]
					Indicator.CatalogName = ""
					Indicator.Code = sheet2.row_values(1)[0]
					Indicator.Unit = ""
					Indicator.Period = "year"
					Indicator.OwnerOrg = sheet2.row_values(1)[3]
					Indicator.NoteLoc['Chinese'] = sheet2.row_values(1)[2]
					
					con.DBStore.DataIndicators.insert(Indicator.ToMap());
					code = Indicator.Code;
				else:
					code = DataIndicators['code'];
				first_row = sheet1.row_values(0)
				for i in range(sheet1.nrows):
					if i > 0:
						for j in range(sheet1.ncols):
							if j > 1:
								# Data value
								if sheet1.row_values(i)[j] != "":
									Data = MetaData()
									Data.IndicatorTypeCode = code
									Data.AreaSC3 = sheet1.row_values(i)[1]
									Data.DataTime = first_row[j]
									Data.RefURL = "http://data.worldbank.org.cn/indicator"
									Data.Value = sheet1.row_values(i)[j]
									Data.UpdateTime = time.strftime()
									con.DBStore.MetaData.insert(Data.ToMap())

									#check if area exist
									Area = con.DBStore.DataIndicators.find_one({"sc3":Data.AreaSC3})
									if Area is None:
										logger.error("Area is not exist : " + Data.AreaSC3)

logger = logging.getLogger() 
file = logging.FileHandler("WorldBank_XLS_Parser.log")
logger.addHandler(file)

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		WorldBank_XLS_Parser()