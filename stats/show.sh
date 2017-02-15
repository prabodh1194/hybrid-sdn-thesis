#!/usr/bin/env bash

echo 's2'
sudo ovs-appctl fdb/show s2
echo 's3'
sudo ovs-appctl fdb/show s3
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
