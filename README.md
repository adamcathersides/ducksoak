# ducksoak

A way of running a load of tsduck docker instances to analyse a bunch of streams.

# Installation

```
cd ducksoak
pip install . --user
```

# Configfile

Its a yaml file.  You can define where you want the logs to go on your localmachine, the tsduck a image to use and what input and output stream you would like to analyse.
Here is an example:
```
image: tsduckimage:1
logs: /tmp/soaklogs
inputs:
    - 239.100.1.1:5000
    - 239.100.1.2:5000
outputs:
    - 239.1.1.1:5000
    - 239.1.1.2:5000
```

# Running

This script will run a tsduck container per input/output stream 
### To make a mess..(normal running)
```
ducksoak config.yaml
```
### To tidy up..

```
ducksoak config.yaml --tidyup
```

# Notes
The tsduck containers are run in host networking mode
