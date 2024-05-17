#!/bin/bash

server_ip="192.168.1.5"
server_port=8081
path_to_scan="/Users/sebastianrivera/Library/CloudStorage/OneDrive-Personal/Computer Science/7to/os/proyecto sincronizacion"

for i in {1..40}
do
    python3 client.py "$server_ip" "$server_port" "$path_to_scan" &
done

wait
