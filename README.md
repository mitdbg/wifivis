# Initial Setup

We include some data already.  Simply decompress the file `util/data.csv.gz`


# Usage


Go to root of the repo and run the server in threaded mode

    python server.py --threaded <IP or Hostname> <PORT>

Navigate your browser to `http://<IP or Hostname>:<PORT>/`



# Prep new wifi data

Add `logs` file in `util/` with schema `timestamp/count/accesspointid`.  It should look like this:

    1411676653,0,0
    1411676653,4,1
    1411676653,6,2
    1411676653,8,3
    1411676653,0,4

cd to `util/`:

    cd util

Join the wifidata with the lat/lon dataset:

    python prepdata > data.csv

go back to the root:

    cd .. 

First few lines in `util/data.csv` should look like:

    time,room,count,lon,lat
    1411725853,nw86-715,1,-71.101716,42.359562
    1411725853,ne47-597,1,-71.092506,42.363297
    1411725853,w1-3037,14,-71.093457,42.357710
    1411725853,w1-3032,5,-71.093457,42.357710



