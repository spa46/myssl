#!/bin/bash

# test_tls_connection.sh

HOST="localhost"
PORT="4443"
CA_FILE="serverCA/ca-chain.pem"

# connect 
output=$(echo "" | openssl s_client -connect ${HOST}:${PORT} \
  -CAfile ${CA_FILE} \
  -verify_return_error \
  -brief 2>&1)

exit_code=$?

# verify
if [ $exit_code -eq 0 ] && echo "$output" | grep -q "Verification: OK"; then
    echo "PASS: TLS connection to ${HOST}:${PORT} successful"
    echo "Certificate verification: OK"
    exit 0
else
    echo "FAIL: TLS connection to ${HOST}:${PORT} failed"
    echo "Exit code: $exit_code"
    echo "$output"
    exit 1
fi
