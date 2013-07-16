
class DataIndicators:
	Name = ""
	LocName = ""
	CatalogName = ""
	Code = ""
	Unit = ""
	Period = ""
	Owner = ""
	Note = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['LocName'] = LocName;
		DataMap['CatalogName'] = CatalogName;
		DataMap['Code'] = Code;
		DataMap['Unit'] = Unit;
		DataMap['Period'] = Period;
		DataMap['Unit'] = Unit;
		DataMap['Note'] = Note;

		return DataMap

class MetaData:

	def ToMap():
		DataMap = {}
		return DataMap

class Area:

	def ToMap():
		DataMap = {}
		return DataMap


