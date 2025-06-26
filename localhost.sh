#!/bin/bash

# Start the AI Flask server in a new Terminal tab
echo "🔥 Starting Local AI Server..."
osascript -e 'tell application "Terminal" to do script "cd \"'"$(pwd)"'\" && python3 local_ai_server.py"'

# Wait a sec to make sure server starts
sleep 3

# Start ngrok tunnel (you must have ngrok installed and authtoken set)
echo "🌐 Starting Ngrok Tunnel..."
osascript -e 'tell application "Terminal" to do script "ngrok http 5000 --log=stdout"'

# Wait for ngrok to actually start
sleep 15

# Try to get the NGROK URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[a-zA-Z0-9.-]*.ngrok-free.app' | head -n 1)

if [ -z "$NGROK_URL" ]; then
    echo "😤 Couldn't fetch NGROK_URL automatically. Try refreshing ngrok or checking the dashboard."
    exit 1
fi

echo "🚀 NGROK URL: $NGROK_URL"
export NGROK_URL=$NGROK_URL

# Final message
echo "🌱 Your AI server is live! SEED can now send prompt2audio tasks here."