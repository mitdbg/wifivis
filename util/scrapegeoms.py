import sys
import pdb
import json
import requests


locs = json.load(file('locs.json'))

urlbase = "https://maps.mit.edu/pub/rest/services/basemap/MIT_Building/MapServer/find?searchText=%s&contains=true&searchFields=&sr=4326&layers=0&layerDefs=&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=pjson"

idx = 0
seen = set()
print "idx,lon,lat"
for (loc, id) in locs.iteritems():
  try:
    blg,rm = loc.split('-')[:2]
    if blg.startswith('m'):
      blg = blg[1:]
    if blg in seen: continue
    seen.add(blg)

    url = urlbase % blg
    results = json.loads(requests.get(url).content)['results']
    for result in results:
      geom = result['geometry']
      rings = geom['rings']
      for ring in rings:
        for lonlat in ring:
          print "%s,%f,%f" % (blg+"-"+str(idx), lonlat[0], lonlat[1])
        idx += 1
    print>>sys.stderr, blg
  except Exception as e:
    print>>sys.stderr, e
    pass




