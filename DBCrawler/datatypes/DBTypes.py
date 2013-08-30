
class IndicatorData:
	Keywords = []
	NameLoc = {}
	SrcTargetID = None
	NoteLoc = {}
	OutURL = ""
	CombinedDataID = None
	SrcURL={}

	def __init__(self):
		self.Keywords = []
		self.NameLoc = {}
		self.SrcTargetID = None
		self.NoteLoc = {}
		self.OutURL = ""
		self.CombinedDataID = None
		self.SrcURL = {}

	def ToMap(self):
		DataMap = {}
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if len(self.Keywords) > 0:
			DataMap['Keywords'] = self.Keywords;
		if self.SrcTargetID != None:
			DataMap['SrcTargetID'] = self.SrcTargetID;
		if len(self.NoteLoc) > 0:
			DataMap['NoteLoc'] = self.NoteLoc;
		if self.OutURL != '':
			DataMap['OutURL'] = self.OutURL;
		if self.CombinedDataID != '':
			DataMap['CombinedDataID'] = self.CombinedDataID;
		if len(self.SrcURL) > 0:
			DataMap['SrcURL'] = self.SrcURL;

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
	NoteLoc = {}
	UpdateTime = ""
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
		self.NoteLoc = {}
		self.UpdateTime = ""

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

		if len(self.NoteLoc) > 0:
			DataMap['NoteLoc'] = self.NoteLoc;
		if self.UpdateTime != '':
			DataMap['UpdateTime'] = self.UpdateTime;

		return DataMap

class AreaData:
	NameLoc = {}
	SC2 = ""
	SC3 = ""
	NC = ""
	NameFull = ""
	AreaType = ""
	BelongAreaID = None
	MapName = ""
	MapPos = ""

	def __init__(self):
		self.NameLoc = {}
		self.SC2 = ""
		self.SC3 = ""
		self.NC = ""
		self.NameFull = ""
		self.AreaType = ""
		self.BelongAreaID = None
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
		if self.BelongAreaID != None:
			DataMap['BelongArea'] = self.BelongAreaID;
		if self.MapName != '':
			DataMap['MapName'] = self.MapName;
		if self.MapPos != '':
			DataMap['MapPos'] = self.MapPos;

		return DataMap


class TargetData:
	NameLoc = {}
	Type = ""
	NoteLoc = {}
	URLs = []

	def __init__(self):
		self.NameLoc = {}
		self.Type = ""
		self.NoteLoc = {}
		self.URLs = []

	def ToMap(self):
		DataMap = {}
		if len(self.URLs) > 0:
			DataMap['URLs'] = self.URLs;
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if self.Type != '':
			DataMap['Type'] = self.Type;
		if len(self.NoteLoc) > 0:
			DataMap['NoteLoc'] = self.NoteLoc;
		return DataMap

class CatalogData:
	Name = ""
	NameLoc = {}
	ParentName = ""

	def __init__(self):
		self.Name = ""
		self.NoteLoc = {}
		self.ParentName = ""

	def ToMap(self):
		DataMap = {}
		if self.Name != '':
			DataMap['Name'] = self.Name;
		if self.ParentName != '':
			DataMap['ParentName'] = self.ParentName;
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		return DataMap