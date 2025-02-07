#! /usr/bin/env sh

. "/opt/bot/venv/bin/activate"

if [ -z "$TOKEN" ]; then
    printf "%s\n" "TOKEN env is not defined" \
                  "exiting..."
    exit 1
fi
if [ -z "$CALENDAR_PATH" ]; then
    printf "%s\n" "CALENDAR_PATH is not defined" \
                  "exiting..."
    exit 1
fi
if [ ! -f "$CALENDAR_PATH" ]; then
    printf "%s\n" "$CALENDAR_PATH doesn't exist" \
                  "exiting..."
    exit 1
fi
printf "%s\n" "starting bot..."
python /opt/bot/src/main.py "$TOKEN" "$CALENDAR_PATH"
