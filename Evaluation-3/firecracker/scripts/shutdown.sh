curl --unix-socket /tmp/firecracker.socket -i \
    -X PUT "http://localhost/actions" \
    -d '{ "action_type": "SendCtrlAltDel" }'