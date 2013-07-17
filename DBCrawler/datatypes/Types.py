
class IndicatorType:
	Name = ""
	NameLoc = ""
	CatalogName = ""
	Code = ""
	Unit = ""
	Period = ""
	OwnerOrg = ""
	Note = ""
	ParentType = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['CatalogName'] = CatalogName;
		DataMap['Code'] = Code;
		DataMap['Unit'] = Unit;
		DataMap['Period'] = Period;
		DataMap['OwnerOrg'] = OwnerOrg;
		DataMap['Note'] = Note;
		DataMap['ParentType'] = ParentType;

		return DataMap

class MetaData:
	IndicatorTypeCode = ""
	AreaSC3 = ""
	Target1 = ""
	Target2 = ""
	DateTime = ""
	RefURL = ""
	Value = ""
	ForcastValue = ""
	ReleaseTime = ""
	GatherTime = ""
	Notes = ""
	def ToMap():
		DataMap = {}
		DataMap['IndicatorTypeCode'] = IndicatorTypeCode;
		DataMap['AreaSC3'] = AreaSC3;
		DataMap['Target1'] = Target1;
		DataMap['Target2'] = Target2;
		DataMap['DateTime'] = DateTime;
		DataMap['RefURL'] = RefURL;
		DataMap['Value'] = Value;
		DataMap['ForcastValue'] = ForcastValue;
		DataMap['ReleaseTime'] = ReleaseTime;
		DataMap['GatherTime'] = GatherTime;
		DataMap['Notes'] = Notes;
		return DataMap

class Area:
	Name = ""
	NameChinese = ""
	NameEnglish = ""
	SC2 = ""
	SC3 = ""
	NC = ""
	NameFull = ""
	AreaType = ""
	BelongArea = ""
	MapName = ""
	MapPos = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameChinese'] = NameChinese;
		DataMap['NameEnglish'] = NameEnglish;
		DataMap['SC2'] = SC2;
		DataMap['SC3'] = SC3;
		DataMap['NC'] = NC;
		DataMap['NameFull'] = NameFull;
		DataMap['AreaType'] = AreaType;
		DataMap['BelongArea'] = BelongArea;
		DataMap['MapName'] = MapName;
		DataMap['MapPos'] = MapPos;
		return DataMap


class Owner:
	Name = ""
	NameLoc = ""
	Type = ""
	Note = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['Type'] = Type;
		DataMap['Note'] = Note;
		return DataMap

class Target:
	Name = ""
	NameLoc = ""
	Type = ""
	Note = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['Type'] = Type;
		DataMap['Note'] = Note;
		return DataMap

class Catalog:
	Name = ""
	NameLoc = ""
	ParentName = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['ParentName'] = ParentName;
		return DataMap

