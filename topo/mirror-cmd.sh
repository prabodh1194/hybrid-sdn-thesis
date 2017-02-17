#!/usr/bin/env bash

sudo ovs-vsctl -- set Bridge s1 mirrors=@m\
               -- --id=@eth1 get Port s1-eth1\
               -- --id=@eth2 get Port s2-eth1\
               -- --id=@eth3 get Port s1-eth3\
               -- --id=@m create Mirror name=mymirror select-dst-port=@eth2,@eth1 select-src-port=@eth1,@eth2 output-port=@eth3
