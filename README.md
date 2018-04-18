jma-ash-info2geojson
======

Volcanic ash Information XML from JMA(Japan Meteorological Agency) to GeoJSON

気象庁防災情報XML電文の**降灰予報（定時）**、**降灰予報（速報）**、**降灰予報（詳細）**から、GeoJSONを生成する

## How to use

```
python ashinfo2geojson.py [uuid].xml
```

※[uuid].xmlは気象庁より配信された降灰予報のXML形式電文ファイル
