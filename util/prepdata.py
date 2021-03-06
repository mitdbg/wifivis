from collections import *
import json


def bad_rooms(mincount):
  counts = defaultdict(lambda: 0)
  for line in file('logs'):
    tstamp,count,id =  line.strip().split(',')
    count = int(count)

    id = int(id)
    rm = id2rm[id]
    rmid = '-'.join(rm.split('-')[:2])
    counts[rmid] = max(counts[rmid], count)

  return [rm for rm, c in counts.iteritems() if c < mincount]


rm2id = json.load(file('locs.json'))
id2rm = {id:rm for rm,id in rm2id.iteritems()}

wifiap = [line.strip().split(',') for line in file('wifiap')][1:]
wifiap = { ('-'.join([line[1],line[2]])) : (float(line[3]), float(line[4])) for line in wifiap}

for rm, id in rm2id.iteritems():
  rmid = '-'.join(rm.split('-')[:2])
  if rmid in wifiap:
    lon, lat = wifiap[rmid]



print "time,room,count,lon,lat"
prevtstamp = None
roomcounts = {}  # room -> (count, lat, lon)
badrooms = set(bad_rooms(10))
print badrooms
for line in file('logs'):
  tstamp,count,id =  line.strip().split(',')
  count = int(count)
  tstamp = int(tstamp)
  if prevtstamp is not None and tstamp != prevtstamp and tstamp - prevtstamp < 60 * 25:
    continue

  if tstamp != prevtstamp:
    prevtstamp = tstamp
    for tup in roomcounts.values():
      print '%s,%s,%s,%f,%f' % tuple(tup)
    roomcounts = {}


  id = int(id)
  rm = id2rm[id]
  rmid = '-'.join(rm.split('-')[:2])
  if rmid in badrooms:
    continue
  if rmid in wifiap:
    lon, lat = wifiap[rmid]
    if lon == 0 or lat == 0: continue
    if rmid not in roomcounts:
      roomcounts[rmid] = [tstamp, rmid, count, lon, lat]
    else:
      roomcounts[rmid][2] += count


for tup in roomcounts.values():
  print '%s,%s,%s,%f,%f' % tuple(tup)

