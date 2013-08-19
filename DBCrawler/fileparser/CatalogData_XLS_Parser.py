#coding=utf-8
import xlrd
import os
import sys
import os.path
import pymongo
import logging
from Data_Manager import CatalogData_Insert

def CatalogData_XLS_Parser():
	#filename = 'E:\Study\Web\Root\DB\Doc\Area.xlsx'
	filename = 'c:\git\DB\Doc\Catalog.xlsx'
	xlsfile = xlrd.open_workbook(filename)
	sheet1 = xlsfile.sheet_by_name("Sheet1")

	#check the data indicator
	for i in range(1, sheet1.nrows):
		id = CatalogData_Insert(con, sheet1.row_values(i)[0], sheet1.row_values(i)[1], sheet1.row_values(i)[2]);
		print id;

logger = logging.getLogger() 
file = logging.FileHandler("CatalogData_XLS_Parser.log")
logger.addHandler(file)

con = pymongo.Connection('localhost', 27017)

if con:
	db = con.DBStore
	if db:
		CatalogData_XLS_Parser()