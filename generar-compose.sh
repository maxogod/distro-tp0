#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <output_file> <number_of_clients>"
    exit 1
fi

output_file=$1
num_clients=$2
content=""

# Insert services
insert_server_service() {
    content+="\n\tserver:\n"
    content+="\t\tcontainer_name: server\n"
    content+="\t\timage: server_image\n"
    content+="\t\tentrypoint: python3 /main.py\n"
    content+="\t\tenvironment:\n"
    content+="\t\t\t- PYTHONUNBUFFERED=1\n"
    content+="\t\tnetworks:\n"
    content+="\t\t\t- testing_net\n"
}

insert_client_services() {
    for ((i=1; i<=num_clients; i++)); do
        content+="\n\tclient$i:\n"
        content+="\t\tcontainer_name: client$i\n"
        content+="\t\timage: client:latest\n"
        content+="\t\tentrypoint: /client\n"
        content+="\t\tenvironment:\n"
        content+="\t\t\t- CLI_ID=$i\n"
        content+="\t\tnetworks:\n"
        content+="\t\t\t- testing_net\n"
        content+="\t\tdepends_on:\n"
        content+="\t\t\t- server\n"
    done
}

# Insert networks
insert_networks() {
    content+="\nnetworks:\n"
    content+="\ttesting_net:\n"
    content+="\t\tipam:\n"
    content+="\t\t\tdriver: default\n"
    content+="\t\t\tconfig:\n"
    content+="\t\t\t\t- subnet: 172.25.125.0/24"
}

# Create content
content+="name: tp0"
content+="\nservices:"
insert_server_service
insert_client_services
insert_networks

# Write content to output file
echo -e $content > $output_file
echo "Docker Compose file generated: $output_file"
