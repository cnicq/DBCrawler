class IndicatorData:
	Keywords = []
	NameLoc = []
	SrcTarget = ""
	Note = ""
	OutURL = ""

	def ToMap(self):
		DataMap = {}
		if len(self.NameLoc) > 0:
			DataMap['NameLoc'] = self.NameLoc;
		if len(self.Keywords) > 0:
			DataMap['Keywords'] = self.Keywords;
		if self.SrcTarget != '':
			DataMap['SrcTarget'] = self.SrcTarget;
		if self.Note != '':
			DataMap['Note'] = self.Note;
		if self.OutURL != '':
			DataMap['OutURL'] = self.OutURL;

		return DataMap

class MetaData:
	AreaID = ""
	Target1ID = ""
	Target2ID = ""
	Period = ""
	Datas = []

	def ToMap():
		DataMap = {}
		if AreaID != '':
			DataMap['AreaID'] = AreaID;
		if Target1ID != '':
			DataMap['Target1ID'] = Target1ID;
		if Target2ID != '':
			DataMap['Target2ID'] = Target2ID;
		if Period != '':
			DataMap['Period'] = Period;
		if len(Datas) > 0:
			DataMap['Datas'] = Datas;

		return DataMap

class AreaData:
	NameLoc = []
	SC2 = ""
	SC3 = ""
	NC = ""
	NameFull = ""
	AreaType = ""
	BelongAreaID = ""
	MapName = ""
	MapPos = ""

	def ToMap():
		DataMap = {}
		if len(NameLoc) > 0:
			DataMap['NameLoc'] = NameLoc;
		if SC2 != '':
			DataMap['SC2'] = SC2;
		if SC3 != '':
			DataMap['SC3'] = SC3;
		if NC != '':
			DataMap['NC'] = NC;
		if NameFull != '':
			DataMap['NameFull'] = NameFull;
		if AreaType != '':
			DataMap['AreaType'] = AreaType;
		if BelongArea != '':
			DataMap['BelongArea'] = BelongArea;
		if MapName != '':
			DataMap['MapName'] = MapName;
		if MapPos != '':
			DataMap['MapPos'] = MapPos;

		return DataMap


class TargetData:
	NameLoc = []
	Type = ""
	Note = ""
	URLs = "[]"

	def ToMap():
		DataMap = {}
		if URLs != '':
			DataMap['URLs'] = URLs;
		if len(NameLoc) > 0:
			DataMap['NameLoc'] = NameLoc;
		if MapPos != '':
			DataMap['Type'] = Type;
		if Note != '':
			DataMap['Note'] = Note;
		return DataMap

class CatalogData:
	NameLoc = []
	ParentName = ""

	def ToMap():
		DataMap = {}
		DataMap['Name'] = Name;
		DataMap['NameLoc'] = NameLoc;
		DataMap['ParentName'] = ParentName;
		return DataMap

