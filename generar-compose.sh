#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <output_file> <number_of_clients>"
    exit 1
fi

output_file=$1
num_clients=$2
indent="  "

indent_string() {
    local level=$1
    local string=$2
    local res=""
    for ((i=0; i<level; i++)); do
        res+=$indent
    done
    res+=$string
    echo -e "$res"
}

insert_server_service() {
    content+="\n$(indent_string 1 "server:")\n"
    content+="$(indent_string 2 "container_name: server")\n"
    content+="$(indent_string 2 "image: server:latest")\n"
    content+="$(indent_string 2 "entrypoint: python3 /main.py")\n"
    content+="$(indent_string 2 "environment:")\n"
    content+="$(indent_string 3 "- PYTHONUNBUFFERED=1")\n"
    content+="$(indent_string 2 "volumes:")\n"
    content+="$(indent_string 3 "- ./server/config.ini:/config.ini")\n"
    content+="$(indent_string 2 "networks:")\n"
    content+="$(indent_string 3 "- testing_net")\n"
}

insert_client_services() {
    for ((i=1; i<=num_clients; i++)); do
        content+="\n$(indent_string 1 "client$i:")\n"
        content+="$(indent_string 2 "container_name: client$i")\n"
        content+="$(indent_string 2 "image: client:latest")\n"
        content+="$(indent_string 2 "entrypoint: /client")\n"
        content+="$(indent_string 2 "environment:")\n"
        content+="$(indent_string 3 "- CLI_ID=$i")\n"
        content+="$(indent_string 3 "- CLI_AGENCY_DATA=/agency.csv")\n"
        content+="$(indent_string 2 "volumes:")\n"
        content+="$(indent_string 3 "- ./client/config.yaml:/config.yaml")\n"
        content+="$(indent_string 3 "- ./.data/agency-$i.csv:/agency.csv")\n"
        content+="$(indent_string 2 "networks:")\n"
        content+="$(indent_string 3 "- testing_net")\n"
        content+="$(indent_string 2 "depends_on:")\n"
        content+="$(indent_string 3 "- server")\n"
    done
}

insert_networks() {
    content+="\nnetworks:\n"
    content+="$(indent_string 1 "testing_net:")\n"
    content+="$(indent_string 2 "ipam:")\n"
    content+="$(indent_string 3 "driver: default")\n"
    content+="$(indent_string 3 "config:")\n"
    content+="$(indent_string 4 "- subnet: 172.25.125.0/24")\n"
}

# Create content
content="name: tp0"
content+="\nservices:"
insert_server_service
insert_client_services
insert_networks

# Write content to output file
echo -e "$content" > "$output_file"
echo "Docker Compose file generated: $output_file"
