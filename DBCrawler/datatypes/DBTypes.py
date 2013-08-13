
class IndicatorData:
	Keywords = []
	NameLoc = {}
	SrcTargetID = None
	Note = ""
	OutURL = ""
	CombinedDataID = None

	def __init__(self):
		self.Keywords = []
		self.NameLoc = {}
		self.SrcTargetID = None
		self.Note = ""
		self.OutURL = ""
		self.CombinedDataID = None

	def ToMap(self):
		DataMap = {}
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if len(self.Keywords) > 0:
			DataMap['Keywords'] = self.Keywords;
		if self.SrcTargetID != None:
			DataMap['SrcTargetID'] = self.SrcTargetID;
		if self.Note != '':
			DataMap['Note'] = self.Note;
		if self.OutURL != '':
			DataMap['OutURL'] = self.OutURL;
		if self.CombinedDataID != '':
			DataMap['CombinedDataID'] = self.CombinedDataID;

		return DataMap

class MetaData:
	AreaID = ""
	Target1ID = None
	Target2ID = None
	Period = ""
	Datas = []

	def __init__(self):
		self.AreaID = ""
		self.Target1ID = None
		self.Target2ID = None
		self.Period = ""
		self.Datas = []

	def ToMap(self):
		DataMap = {}
		if self.AreaID != None:
			DataMap['AreaID'] = self.AreaID;
		if self.Target1ID != None:
			DataMap['Target1ID'] = self.Target1ID;
		if self.Target2ID != None:
			DataMap['Target2ID'] = self.Target2ID;
		if self.Period != '':
			DataMap['Period'] = self.Period;
		if len(self.Datas) > 0:
			DataMap['Datas'] = self.Datas;

		return DataMap

class CombinedData:
	Conditions = []
	NameLoc = {}
	Star = 0
	Follow = 0
	Comments = 0
	Views = 0
	Catalogs = []
	Note = {}
	LastUpdate = ""
	CombinedType = 0


	def __init__(self):
		self.Conditions = []
		self.NameLoc = {}
		self.Catalogs = []
		self.Star = 0
		self.Follow = 0
		self.Comments = 0
		self.Views = 0
		self.CombinedType = 0
		self.Note = ""
		self.LastUpdate = ""

	def ToMap(self):
		DataMap = {}
		if len(self.Conditions) > 0:
			DataMap['Conditions'] = self.Conditions;
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if len(self.Catalogs) > 0:
			DataMap['Catalogs'] = self.Catalogs;
		DataMap['Star'] = self.Star;
		DataMap['Follow'] = self.Follow;
		DataMap['Comments'] = self.Comments;
		DataMap['Views'] = self.Views;
		DataMap['CombinedType'] = self.CombinedType;

		if self.Note != '':
			DataMap['Note'] = self.Note;
		if self.LastUpdate != '':
			DataMap['LastUpdate'] = self.LastUpdate;

		return DataMap

class AreaData:
	NameLoc = {}
	SC2 = ""
	SC3 = ""
	NC = ""
	NameFull = ""
	AreaType = ""
	BelongAreaID = ""
	MapName = ""
	MapPos = ""

	def __init__(self):
		self.NameLoc = {}
		self.SC2 = ""
		self.SC3 = ""
		self.NC = ""
		self.NameFull = ""
		self.AreaType = ""
		self.BelongAreaID = ""
		self.MapName = ""
		self.MapPos = ""
	def ToMap(self):
		DataMap = {}
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if self.SC2 != '':
			DataMap['SC2'] = self.SC2;
		if self.SC3 != '':
			DataMap['SC3'] = self.SC3;
		if self.NC != '':
			DataMap['NC'] = self.NC;
		if self.NameFull != '':
			DataMap['NameFull'] = self.NameFull;
		if self.AreaType != '':
			DataMap['AreaType'] = self.AreaType;
		if self.BelongAreaID != '':
			DataMap['BelongArea'] = self.BelongAreaID;
		if self.MapName != '':
			DataMap['MapName'] = self.MapName;
		if self.MapPos != '':
			DataMap['MapPos'] = self.MapPos;

		return DataMap


class TargetData:
	NameLoc = {}
	Type = ""
	Note = ""
	URLs = []

	def __init__(self):
		self.NameLoc = {}
		self.Type = ""
		self.Note = ""
		self.URLs = []

	def ToMap(self):
		DataMap = {}
		if len(self.URLs) > 0:
			DataMap['URLs'] = self.URLs;
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if self.Type != '':
			DataMap['Type'] = self.Type;
		if self.Note != '':
			DataMap['Note'] = self.Note;
		return DataMap

class CatalogData:
	NameLoc = {}
	ParentName = ""

	def ToMap(self):
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['ParentName'] = ParentName;
		return DataMap