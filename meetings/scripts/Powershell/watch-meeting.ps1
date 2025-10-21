# watch-meeting.ps1
# PowerShell script to manage meeting messages and monitor for changes

param(
    [Parameter(Mandatory=$true)]
    [string]$Persona,
    
    [Parameter(Mandatory=$false)]
    [string]$MeetingFile = "meetings/meeting.md",
    
    [Parameter(Mandatory=$false)]
    [string]$Message = "",
    
    [Parameter(Mandatory=$false)]
    [int]$ContextMessages = 5,
    
    [Parameter(Mandatory=$false)]
    [switch]$EndMeeting,
    
    [Parameter(Mandatory=$false)]
    [switch]$Fetch
)

# Configuration
$TimeoutSeconds = 300  # 5 minute timeout to prevent infinite waiting

# Validate meeting file exists
if (-not (Test-Path $MeetingFile)) {
    Write-Host "ERROR: Meeting file not found: $MeetingFile" -ForegroundColor Red
    Write-Host "Please ensure the meeting file exists before starting the watch." -ForegroundColor Yellow
    exit 1
}

# If EndMeeting flag is set, change Status to COMPLETE and exit
if ($EndMeeting) {
    try {
        $content = Get-Content $MeetingFile -Raw
        if ($content -match '(?m)^\*\*Status:\*\*\s+\w+') {
            $newContent = $content -replace '(?m)(^\*\*Status:\*\*\s+)\w+', '${1}COMPLETE'
            Set-Content -Path $MeetingFile -Value $newContent -NoNewline
            Write-Host "[$Persona] Meeting Status changed to COMPLETE" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "[$Persona] ERROR: Could not find Status field in meeting file" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "[$Persona] Error updating meeting status: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# If message provided, append it to the meeting file
if ($Message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $formattedMessage = "`n**[$Persona - $timestamp]:** $Message`n"
    
    try {
        Add-Content -Path $MeetingFile -Value $formattedMessage -NoNewline
        Write-Host "[$Persona] Message posted at $timestamp" -ForegroundColor Green
    } catch {
        Write-Host "[$Persona] Error writing message: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# If Fetch flag is set, just display current meeting content and exit (no monitoring)
if ($Fetch) {
    Write-Host "[$Persona] Fetching current meeting content..." -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Cyan
    
    try {
        $currentContent = Get-Content $MeetingFile -Raw -ErrorAction SilentlyContinue
        if ($null -ne $currentContent) {
            # Show the current Status
            if ($currentContent -match '(?m)^\*\*Status:\*\*\s+(\w+)') {
                $currentStatus = $matches[1]
                Write-Host "Current Status: $currentStatus" -ForegroundColor $(if ($currentStatus -eq "COMPLETE") { "Yellow" } else { "Green" })
                Write-Host ""
            }
            
            # Extract and display transcript messages
            if ($currentContent -match '(?s)## Transcript\s*(.+)') {
                $transcriptContent = $matches[1]
                $messagePattern = '\*\*\[.+?\]:\*\*.+'
                $messages = [regex]::Matches($transcriptContent, $messagePattern)
                
                if ($messages.Count -gt 0) {
                    # Show last N messages for context
                    $startIndex = [Math]::Max(0, $messages.Count - $ContextMessages)
                    for ($i = $startIndex; $i -lt $messages.Count; $i++) {
                        Write-Host $messages[$i].Value
                    }
                } else {
                    Write-Host "No messages found in transcript section"
                }
            } else {
                # Fallback: show full content if we can't parse transcript
                Write-Host $currentContent
            }
        } else {
            Write-Host "ERROR: Could not read meeting file content" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "[$Persona] Error reading file: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "[$Persona] Fetch complete. Use -Message to respond." -ForegroundColor Green
    exit 0
}

Write-Host "[$Persona] Monitoring meeting file: $MeetingFile" -ForegroundColor Green

try {
    # Get initial file info and content
    $initialInfo = Get-Item $MeetingFile
    $initialContent = Get-Content $MeetingFile -Raw -ErrorAction SilentlyContinue
    $startTime = Get-Date
    
    # Check if meeting is already complete
    if ($initialContent -match '(?m)^\*\*Status:\*\*\s+COMPLETE') {
        Write-Host "[$Persona] Meeting Status is COMPLETE. Exiting..." -ForegroundColor Yellow
        exit 0
    }
    
    Write-Host "[$Persona] Waiting for file changes..." -ForegroundColor Yellow
    
    # Monitor for file changes or status change
    do {
        Start-Sleep -Milliseconds 500
        
        # Check for timeout
        $elapsed = (Get-Date) - $startTime
        if ($elapsed.TotalSeconds -gt $TimeoutSeconds) {
            Write-Host "[$Persona] Timeout reached. Checking meeting status..." -ForegroundColor Yellow
            break
        }
        
        # Check if file was modified
        $currentInfo = Get-Item $MeetingFile -ErrorAction SilentlyContinue
        if ($null -eq $currentInfo) {
            Write-Host "[$Persona] Meeting file was deleted or moved." -ForegroundColor Red
            exit 1
        }
        
        # If file changed, check if Status changed to COMPLETE
        if ($currentInfo.LastWriteTime -ne $initialInfo.LastWriteTime) {
            $currentContent = Get-Content $MeetingFile -Raw -ErrorAction SilentlyContinue
            if ($currentContent -match '(?m)^\*\*Status:\*\*\s+COMPLETE') {
                Write-Host "[$Persona] Meeting Status changed to COMPLETE!" -ForegroundColor Green
                break
            }
            # File changed but status still ACTIVE
            break
        }
        
    } while ($true)
    
    # File changed or timeout - output meeting content
    Write-Host "`n[$Persona] File change detected! Reading new content..." -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Cyan
    
    # Read and display NEW content (what changed since we started monitoring)
    $newContent = Get-Content $MeetingFile -Raw -ErrorAction SilentlyContinue
    if ($null -ne $newContent) {
        # First, show the current Status
        if ($newContent -match '(?m)^\*\*Status:\*\*\s+(\w+)') {
            $currentStatus = $matches[1]
            Write-Host "Current Status: $currentStatus" -ForegroundColor $(if ($currentStatus -eq "COMPLETE") { "Yellow" } else { "Green" })
            Write-Host ""
        }
        
        # Extract just the new messages (after the Transcript section)
        if ($newContent -match '(?s)## Transcript\s*(.+)') {
            $transcriptContent = $matches[1]
            # Get the last few messages for context
            $messagePattern = '\*\*\[.+?\]:\*\*.+'
            $messages = [regex]::Matches($transcriptContent, $messagePattern)
            
            if ($messages.Count -gt 0) {
                # Show last N messages for context (configurable via -ContextMessages parameter)
                $startIndex = [Math]::Max(0, $messages.Count - $ContextMessages)
                for ($i = $startIndex; $i -lt $messages.Count; $i++) {
                    Write-Host $messages[$i].Value
                }
            } else {
                Write-Host "No messages found in transcript section"
            }
        } else {
            # Fallback: show full content if we can't parse transcript
            Write-Host $newContent
        }
    } else {
        Write-Host "ERROR: Could not read meeting file content" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "[$Persona] Review the content above and respond if appropriate." -ForegroundColor Green
    Write-Host "[$Persona] To respond: Run script again with -Message parameter" -ForegroundColor Yellow
    Write-Host "[$Persona] If Status is COMPLETE, do not restart monitoring." -ForegroundColor Yellow
    
} catch {
    Write-Host "[$Persona] Error monitoring file: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "[$Persona] Closing terminal..." -ForegroundColor Yellow
    Start-Sleep -Seconds 1
    [Environment]::Exit(1)
}

# Exit with success to wake the agent and close terminal
Write-Host "[$Persona] Script complete. Terminal will remain open for review." -ForegroundColor Green
Write-Host "[$Persona] You can manually close this terminal or it will be reused for the next command." -ForegroundColor Yellow
Start-Sleep -Seconds 2
exit 0