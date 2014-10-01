import sys
import pdb
import json
import requests


urlbase = "http://maps-svcs.mit.edu/pub/rest/services/locators/mit_campus_geocode/GeocodeServer/findAddressCandidates?SingleKey=%s&Single+Line+Input=&outFields=&maxLocations=&outSR=4326&searchExtent=&f=pjson"
locs = json.load(file('locs.json'))

if False:
  for loc in locs.keys():
    if loc.startswith('oc'):
      print loc
    if loc.startswith('bent'):
      print loc
    if loc.startswith('ee'):
      print loc
    if loc.startswith('albanyst'):
      print loc
    if loc.startswith('eduroam'):
      print loc
  exit()

  x = set()
  bad = ['-'] + map(str,range(11))
  for loc in set([loc for loc in locs.keys()]):
    good = []
    for c in loc:
      if c in bad: break
      good.append(c)
    loc = ''.join(good)
    x.add(loc)
  for loc in x: print loc
  exit()


print "id,blg,rm,lon,lat,idx"
for idx, (loc, id) in enumerate(locs.iteritems()):
  try:
    blg,rm = loc.split('-')[:2]
    room = '-'.join((blg, rm))
    if room.startswith('m'):
      room = room[1:]

    url = urlbase % room
    cands = json.loads(requests.get(url).content)['candidates']
    if not cands:
      url = urlbase % blg
      cands = json.loads(requests.get(url).content)['candidates']

    if cands:
      location = cands[0]['location']
      lon = location['x']
      lat = location['y']
      print "%d,%s,%s,%f,%f,%s" % (id, blg, rm, lon, lat, idx)
    else:
      print>> sys.stderr, "couldn't map: %s" % (room)
  except Exception as e:
    print >> sys.stderr, str(e)
