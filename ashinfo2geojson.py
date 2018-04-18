import sys
import json
import xml.etree.ElementTree as et
from collections import defaultdict

namespaces = {
    'jmx_ib': 'http://xml.kishou.go.jp/jmaxml1/informationBasis1/',
    'jmx_eb': 'http://xml.kishou.go.jp/jmaxml1/elementBasis1/',
    'jmx_vc': 'http://xml.kishou.go.jp/jmaxml1/body/volcanology1/'
    }

def tag(namespace, element):
    return '{' + namespaces[namespace]+ '}'+ element

class AshInfo:
    def __init__(self, tree):
        self.tree = tree
        self.parse()

    def parse(self):
        root = self.tree.getroot()

        head = root.find('.//jmx_ib:Head', namespaces)
        self.headTitle = head.find('.//jmx_ib:Title', namespaces).text
        self.headReportDateTime = head.find('.//jmx_ib:ReportDateTime', namespaces).text
        self.headTargetDateTime = head.find('.//jmx_ib:TargetDateTime', namespaces).text
        self.headValidDateTime = head.find('.//jmx_ib:ValidDateTime', namespaces).text
        self.headEventID = head.find('.//jmx_ib:EventID', namespaces).text
        self.headInfoType = head.find('.//jmx_ib:InfoType', namespaces).text
        self.headSerial = head.find('.//jmx_ib:Serial', namespaces).text
        self.headInfoKind = head.find('.//jmx_ib:InfoKind', namespaces).text
        self.headInfoKindVersion = head.find('.//jmx_ib:InfoKindVersion', namespaces).text
        headline = head.find('.//jmx_ib:Headline', namespaces)
        self.headlineText = headline.find('.//jmx_ib:Text', namespaces).text

        features = []
        ashinfos = root.findall('.//jmx_vc:AshInfo', namespaces)

        for ashinfo in ashinfos:
            aType = ashinfo.get("type")
            for item in ashinfo.findall('.//jmx_vc:Item', namespaces):
                for kind in item.find('.//jmx_vc:Kind', namespaces):
                    if kind.tag == tag('jmx_vc', 'Name'):
                        kName = kind.text
                    elif kind.tag == tag('jmx_vc', 'Property'):
                        polygons = []
                        for property_ in kind:
                            if property_.tag == tag('jmx_eb', 'Polygon'):
                                polygon = []
                                for combined_coordinates in property_.text.split("/"):
                                    if combined_coordinates:
                                        divided_coordinates = combined_coordinates.split("+")
                                        coordinates = [float(divided_coordinates[2]), float(divided_coordinates[1])]
                                        polygon.append(coordinates)
                                polygons.append(polygon)
                            elif property_.tag == tag('jmx_eb', 'PlumeDirection'):
                                direction = property_.get("description")
                            elif property_.tag == tag('jmx_vc', 'Distance'):
                                distance = property_.text
                
                areaList = []
                for areas in item.find('.//jmx_vc:Areas', namespaces):
                    for area in areas:
                        if area.tag == tag('jmx_vc', 'Name'):
                            areaList.append(area.text)
                
                feature = {
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": polygons
                    },
                    "type": "Feature",
                    "properties": {
                        "type": aType,
                        "name": kName,
                        "direction": direction,
                        "distance": distance,
                        "areas": areaList
                    }
                }
                features.append(feature)
        self.featurecollection = {"type":"FeatureCollection","features":features}
        self.geojson = json.dumps(self.featurecollection, ensure_ascii=False)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print('Usage: # python %s uuid.xml ' % argvs[0])
        quit()
    else:
        tree = et.parse(argvs[1])
        ashinfo = AshInfo(tree)
        print(ashinfo.headTitle)
        f = open("output.json", "w")
        f.write(ashinfo.geojson)
        f.close()
        print("save to output.json")