import xlrd
import os
import sys
import os.path
import pymongo

def WorldBank_XLS_Parser():
	for dirpath, dirnames, filenames in os.walk('E:\\Study\\Web\\Root\\DBCrawler\\DBCrawler\\media\\files'):
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
					con.DBStore.DataIndicators.insert({'code':sheet2.row_values(1)[0],
						'name':sheet2.row_values(1)[1],
						'note':sheet2.row_values(1)[2],
						'org':sheet2.row_values(1)[3]});
					code = sheet2.row_values(1)[0];
				else:
					code = DataIndicators['code'];
				first_row = sheet1.row_values(0)
				for i in range(sheet1.nrows):
					if i > 0:
						for j in range(sheet1.ncols):
							if j > 1:
								# Data value
								if sheet1.row_values(i)[j] != "":
									data = {}
									data['country'] = sheet1.row_values(i)[1]
									data['value'] = sheet1.row_values(i)[j]
									data['date'] = first_row[j]
									data['code'] = code
									print data
									con.DBStore.MetaData.insert(data)


con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		WorldBank_XLS_Parser()