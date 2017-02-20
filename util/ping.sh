#!/usr/bin/env bash

for i in {1..64}
do
    ping 10.0.0.$i -c1
done
