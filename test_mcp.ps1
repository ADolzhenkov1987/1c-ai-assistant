# test_mcp.ps1 - MCP server test (UTF-8 output fixed)
$ErrorActionPreference = "Stop"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null

$url = "http://localhost:8000/mcp"
$headers = @{ Accept = "application/json, text/event-stream" }

function Get-BodyUtf8($resp) {
    # PS 5.1 mis-decodes UTF-8 without charset in Content-Type: decode manually
    [System.Text.Encoding]::UTF8.GetString($resp.RawContentStream.ToArray())
}

# --- Step 1: initialize ---
$body = @'
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "test-client", "version": "1.0"}
  }
}
'@

Write-Host "`n=== Step 1: initialize ===" -ForegroundColor Cyan
$resp = Invoke-WebRequest -Uri $url -Method Post `
  -ContentType "application/json; charset=utf-8" -Headers $headers -Body $body

Write-Host "Status: $($resp.StatusCode)"
Write-Host (Get-BodyUtf8 $resp)
Write-Host ""

# Session header: present in stateful mode, absent in stateless mode
$sessionId = $null
foreach ($key in $resp.Headers.Keys) {
    if ($key -ieq "mcp-session-id") {
        $sessionId = $resp.Headers[$key]
        break
    }
}
if ($sessionId) {
    Write-Host "Session ID: $sessionId" -ForegroundColor Green
    $headers = $headers + @{ "mcp-session-id" = $sessionId }
} else {
    Write-Host "No session header (stateless mode - that's fine)" -ForegroundColor Yellow
}
Write-Host ""

# --- Step 2: notifications/initialized ---
$notif = '{"jsonrpc":"2.0","method":"notifications/initialized"}'
Write-Host "=== Step 2: notifications/initialized ===" -ForegroundColor Cyan
try {
    Invoke-WebRequest -Uri $url -Method Post `
      -ContentType "application/json; charset=utf-8" -Headers $headers -Body $notif | Out-Null
    Write-Host "OK"
} catch {
    Write-Host "Notification skipped (acceptable in stateless mode)" -ForegroundColor Yellow
}
Write-Host ""

# --- Step 3: tools/list ---
$listBody = '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
Write-Host "=== Step 3: tools/list ===" -ForegroundColor Cyan
$respList = Invoke-WebRequest -Uri $url -Method Post `
  -ContentType "application/json; charset=utf-8" -Headers $headers -Body $listBody
Write-Host (Get-BodyUtf8 $respList)
Write-Host ""

# --- Step 4: tools/call ---
$callBody = @'
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "ask_1c_assistant",
    "arguments": {
      "question": "Kak obyavit massiv v 1S?",
      "user_id": "test-1"
    }
  }
}
'@

Write-Host "=== Step 4: tools/call (agent request, may take a while) ===" -ForegroundColor Cyan
$respCall = Invoke-WebRequest -Uri $url -Method Post `
  -ContentType "application/json; charset=utf-8" -Headers $headers -Body $callBody -TimeoutSec 120
Write-Host (Get-BodyUtf8 $respCall)
Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green