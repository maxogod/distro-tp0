#!/bin/bash


network_name="tp0_testing_net"
success_message="action: test_echo_server | result: success"
failure_message="action: test_echo_server | result: fail"

validate_server() {
    docker run --network $network_name --rm busybox:latest sh -c '[ "$(echo test message | nc server 12345)" = "test message" ]'

    if [ $? = 0 ]; then
        echo $success_message
    else
        echo $failure_message
    fi
}

validate_server
