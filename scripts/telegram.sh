ga #!/usr/bin/env bash
# Usage:
# API_TOKEN=XXX CHAT_ID=XXX ./telegram.sh "Task is done."
# Note: make it silent: !! &>/dev/null

API_TOKEN=${API_TOKEN}
CHAT_ID=${CHAT_ID}

send() {
        curl -s \
        -X POST \
        https://api.telegram.org/bot$API_TOKEN/sendMessage \
        -d text="$*" \
        -d chat_id=$CHAT_ID
}

if [ $# -eq 0 ]; then
        echo "Nothing to send."
        exit 1
else
        send "$*"
        echo
fi
