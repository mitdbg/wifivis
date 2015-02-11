import pdb
import sys
import os
import json
import time
import requests
from datetime import date, datetime
from datahub import DataHub
from datahub.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient
from thrift.transport import TTransport


# user/password for datahub
DHUSER = ""
DHPASS = ""

# user/password for is&t scraper url
ISTUSER = ""
ISTPASS = ""

try:
  transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = DataHub.Client(protocol)
  con_params = ConnectionParams(user=DHUSER, password=DHPASS)
  con = client.open_connection(con_params=con_params)

  res = client.execute_sql(
    con=con,
    query='create table if not exists wifi.wifi (tstamp bigint,count int,id int)',
    query_params=None)

  client.execute_sql(
    con=con,
    query = 'insert into wifi.wifi values(%d,%d,%d)' % (1,2,1),
    query_params=None
  )

except Exception, e:
  print e

loc2id = {}
keys = None
prev = time.time() - 5*70
now = date.today()
f = None
while True:

  if time.time() - prev < 5 * 60:
    sleeplength = 5*60 - (time.time()-prev)
    print "sleeping at %s for %s seconds" % (datetime.now(), sleeplength)
    time.sleep(sleeplength)

  try:

    if f is None or now != date.today():
      if f:
        f.close()

      now = date.today()
      f = file('/data/sirrice/wifilogs/log_%s' % now, 'a')


    prev = int(time.time())
    try:
      r = requests.get('https://nist-data.mit.edu/wireless/clients.cgi', auth=(ISTUSER, ISTPASS))
      rows = json.loads(r.content)
    except Exception as e:
      print >>sys.stderr, e
      print >>sys.stderr, datetime.now()
      try:
        print >>sys.stderr, "content length: %d" % len(r.content)
      except:
        pass


    if keys is None:
      keys = rows[0].keys()


    if keys is not None:
      towrite = []
      for row in rows:
        row = [row[key] for idx, key in enumerate(keys) if idx != 2]
        count = row[0]
        loc = row[-1]
        if loc not in loc2id:
          loc2id[loc] = len(loc2id)
        towrite.append((prev, count, loc2id[loc]))

      towritestr = '\n'.join([('%d,%d,%d') % x for x in  towrite])
      f.write(towritestr)
      f.flush()

      # now write to last-5 minute file
      with file('/data/sirrice/wifilogs/now', 'w') as nowf:
        nowf.write(towritestr)
      print "wrote %d rows" % len(rows)

      with file("/data/sirrice/wifilogs/locs.json", 'w') as df:
        df.write(json.dumps(loc2id))


      
      try:    
        for x in towrite:
          client.execute_sql(
            con=con,
            query = 'insert into wifi.wifi values(%d,%d,%d)' % x,
            query_params=None
          )
      except Exception, e:
        print "failed write to datahub"


  except Exception as e:
    print >>sys.stderr, e
