#coding=utf-8
import csv
import os
import sys
import os.path
import pymongo
import logging
from DBCrawler.datatypes.Types import IndicatorType,MetaData,Target


def IndicatorType_Parser(csvline):
	#add indicator type and catelog type if not found
	DataType = IndicatorType()
	#DataType.NameLoc = csvline[1]
	#print DataType
	return DataType.Code;

def SubType_Parser(csvline, parentTypeCode):
	for name in csvline:
		DataType = IndicatorType()
		DataType.NameLoc = name
		DataType.ParentType = parentTypeCode
		DataType.Code = ""
		DataType.CatalogName = ""

def Target_Parser(name):
	target = Target()
	target.NameLoc = name
	print target;

def Area_Add(areaName):
	# add new area if not found
	AreaSC3 = ""
	return AreaSC3

def Area_Parser(csvlines):
	n = 0;
	for line in csvlines:
		if n > 2:
			str = line.split(',');
			data = MetaData()
			data.AreaSC3 = Area_Add(str[1])
			if not isdigit(data[1]):
				print ""
def Line_Parser(index, line, IsArea):
	if line[0] == "":
		return
	if 
	try:
		fValue = float(line)
	exception:

def Sina_CSV_Parser():
	for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\sina'):
		for filename in filenames:
			if os.path.splitext(filename)[1] == '.csv':
				filepath = os.path.join(dirpath, filename)
				csvlines = csv.reader(open(filepath, 'r'))
				lines = {}
				IndicatorTypeCode = ""
				n = 0
				IsArea = False
				HasSubType = False
				# 1.record lines and infos
				for line in csvlines:
					lines[n] = line;
					n += 1

				# 2.if second col of third row can not canvert to float, ot check if it's area
				if u'地区' in lines[2][1].replace(' ','').decode('gbk'):
					IsArea = True
				if lines[3][0] == '' and lines[3][1] != "":
					HasSubType = True
					
				# 3.iterator the rows	
				for i in range(starIndex, len(lines)):
					if lines[i][0] == "":
						continue;

				# if u'同比' u'环比', continue

				# 4.if col value is empty, jump to next col
				# 5.if col is float value, check to add indicator type and sub type and metadata to mongodb.
'''			
				IndicatorTypeCode = IndicatorType_Parser(first4lines[0]);
				try:
					fValue = float(strValue)
				exception:
					fvalue = 0.0
				if u'地区' in first4lines[2][0].replace(' ','').decode('gbk'):
					del first4lines[2][0]
					del first4lines[2][1]
					SubType_Parser(first4lines[2], IndicatorTypeCode)
				if first4lines[3][0] == "":
					del first4lines[3][0]
					del first4lines[3][1]
					SubType_Parser(first4lines[3], IndicatorTypeCode)
					print first4lines[0][0].split('_')[2]
				
				for line in csvlines:
					n += 1

				IndicatorType_Parser(csvlines[0])

				if csvlines[2].split(',')[1] == 'Area' or csvlines[3].split(',')[1] == 'Area':
					Area_Parser(csvlines)
				if csvlines[3].split(',')[0] == "":
					SubType_Add(csvlines[3])

				DataIndicators = con.DBStore.DataIndicators.find_one({"code":sheet2.row_values(1)[0]})
				code = "";
				if DataIndicators is None:
					Indicator = IndicatorType();
					Indicator.Name = sheet2.row_values(1)[0]
					Indicator.NameLoc = sheet2.row_values(1)[1]
					Indicator.CatalogName = ""
					Indicator.Code = sheet2.row_values(1)[0]
					Indicator.Unit = ""
					Indicator.Period = "Year"
					Indicator.OwnerOrg = sheet2.row_values(1)[3]
					Indicator.Note = sheet2.row_values(1)[2]
					
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
'''

logger = logging.getLogger() 
file = logging.FileHandler("Sina_XLS_Parser.log")
logger.addHandler(file)

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		Sina_CSV_Parser()