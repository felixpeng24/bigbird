#!/usr/bin/env bash
set -euo pipefail

# Start server in background with output redirected
python server.py > /dev/null 2>&1 &
SERVER_PID=$!
trap "kill $SERVER_PID 2>/dev/null; wait $SERVER_PID 2>/dev/null" EXIT

# Wait for server to be ready
for i in $(seq 1 30); do
  curl -s http://localhost:8080/ > /dev/null 2>&1 && break
  sleep 0.5
done

# Test 1: MJPEG endpoint returns multipart content
echo "Test 1: MJPEG stream..."
CONTENT_TYPE=$(curl -sI --max-time 5 http://localhost:8080/api/video_feed | grep -i content-type | head -1)
echo "$CONTENT_TYPE" | grep -qi "multipart/x-mixed-replace" || { echo "FAIL: MJPEG content type"; exit 1; }
echo "PASS: MJPEG stream returns multipart content type"

# Test 2: Capture endpoint returns base64 JSON
echo "Test 2: Capture endpoint..."
CAPTURE=$(curl -s -X POST http://localhost:8080/api/capture)
echo "$CAPTURE" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'image' in d; import base64; b=base64.b64decode(d['image']); assert b[:2]==b'\xff\xd8'; print(f'PASS: Capture returns valid JPEG ({len(b)} bytes)')"

# Test 3: Index page loads
echo "Test 3: Index page..."
curl -s http://localhost:8080/ | grep -q "BIG BIRD IS WATCHING YOU" || { echo "FAIL: index page missing title"; exit 1; }
echo "PASS: Index page contains title"

echo ""
echo "All S01 verification checks passed."
