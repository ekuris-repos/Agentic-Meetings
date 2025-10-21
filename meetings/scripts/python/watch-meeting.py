#!/usr/bin/env python3
"""
watch-meeting.py
Python script to manage meeting messages and monitor for changes

Usage:
    python watch-meeting.py --persona "Agent-Name" --meeting-file "path/to/meeting.md" [options]

Options:
    --persona, -p          [Required] Agent persona name
    --meeting-file, -f     Meeting file path (default: "meetings/meeting.md")
    --message, -m          Message to post to the meeting
    --context-messages, -c Number of recent messages to display (default: 5)
    --end-meeting, -e      Flag to end the meeting (sets Status to COMPLETE)
    --fetch                Fetch current content without monitoring
    --help, -h             Show this help message
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'

# Configuration
TIMEOUT_SECONDS = 300  # 5 minute timeout
POLL_INTERVAL_SECONDS = 0.5

def log(persona: str, message: str, color: str = Colors.RESET) -> None:
    """Print a colored log message."""
    print(f"{color}[{persona}] {message}{Colors.RESET}")

def print_separator(char: str = '=', length: int = 60) -> None:
    """Print a separator line."""
    print(f"{Colors.CYAN}{char * length}{Colors.RESET}")

def extract_messages(content: str) -> List[str]:
    """Extract messages from the transcript section."""
    match = re.search(r'## Transcript\s*(.*)', content, re.DOTALL)
    if not match:
        return []
    
    transcript_content = match.group(1)
    message_pattern = r'\*\*\[.+?\]:\*\*.+'
    return re.findall(message_pattern, transcript_content)

def extract_status(content: str) -> Optional[str]:
    """Extract the current status from the meeting file."""
    match = re.search(r'^\*\*Status:\*\*\s+(\w+)', content, re.MULTILINE)
    return match.group(1) if match else None

def display_messages(messages: List[str], context_messages: int) -> None:
    """Display the last N messages."""
    if not messages:
        print('No messages found in transcript section')
        return
    
    start_index = max(0, len(messages) - context_messages)
    for message in messages[start_index:]:
        print(message)

def end_meeting(persona: str, meeting_file: str) -> None:
    """Change meeting status to COMPLETE and exit."""
    try:
        with open(meeting_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if re.search(r'^\*\*Status:\*\*\s+\w+', content, re.MULTILINE):
            new_content = re.sub(
                r'^(\*\*Status:\*\*\s+)\w+',
                r'\1COMPLETE',
                content,
                flags=re.MULTILINE
            )
            with open(meeting_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            log(persona, 'Meeting Status changed to COMPLETE', Colors.GREEN)
            sys.exit(0)
        else:
            log(persona, 'ERROR: Could not find Status field in meeting file', Colors.RED)
            sys.exit(1)
    except Exception as e:
        log(persona, f'Error updating meeting status: {e}', Colors.RED)
        sys.exit(1)

def post_message(persona: str, meeting_file: str, message: str) -> None:
    """Append a timestamped message to the meeting file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"\n**[{persona} - {timestamp}]:** {message}\n"
    
    try:
        with open(meeting_file, 'a', encoding='utf-8') as f:
            f.write(formatted_message)
        log(persona, f'Message posted at {timestamp}', Colors.GREEN)
    except Exception as e:
        log(persona, f'Error writing message: {e}', Colors.RED)
        sys.exit(1)

def fetch_content(persona: str, meeting_file: str, context_messages: int) -> None:
    """Fetch and display current meeting content without monitoring."""
    log(persona, 'Fetching current meeting content...', Colors.GREEN)
    print_separator()
    
    try:
        with open(meeting_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        status = extract_status(content)
        if status:
            color = Colors.YELLOW if status == 'COMPLETE' else Colors.GREEN
            log(persona, f'Current Status: {status}', color)
            print()
        
        messages = extract_messages(content)
        display_messages(messages, context_messages)
    except Exception as e:
        log(persona, f'Error reading file: {e}', Colors.RED)
        sys.exit(1)
    
    print_separator()
    log(persona, 'Fetch complete. Use --message to respond.', Colors.GREEN)
    sys.exit(0)

def monitor_file(persona: str, meeting_file: str, context_messages: int) -> None:
    """Monitor the meeting file for changes."""
    log(persona, f'Monitoring meeting file: {meeting_file}', Colors.GREEN)
    
    try:
        # Get initial file stats and content
        file_path = Path(meeting_file)
        initial_mtime = file_path.stat().st_mtime
        
        with open(meeting_file, 'r', encoding='utf-8') as f:
            initial_content = f.read()
        
        start_time = time.time()
        
        # Check if meeting is already complete
        initial_status = extract_status(initial_content)
        if initial_status == 'COMPLETE':
            log(persona, 'Meeting Status is COMPLETE. Exiting...', Colors.YELLOW)
            sys.exit(0)
        
        log(persona, 'Waiting for file changes...', Colors.YELLOW)
        
        # Monitor for file changes
        while True:
            # Check for timeout
            elapsed = time.time() - start_time
            if elapsed > TIMEOUT_SECONDS:
                log(persona, 'Timeout reached. Checking meeting status...', Colors.YELLOW)
                break
            
            # Check if file was modified
            try:
                current_mtime = file_path.stat().st_mtime
                
                if current_mtime != initial_mtime:
                    # File changed - check if status changed to COMPLETE
                    with open(meeting_file, 'r', encoding='utf-8') as f:
                        current_content = f.read()
                    
                    current_status = extract_status(current_content)
                    if current_status == 'COMPLETE':
                        log(persona, 'Meeting Status changed to COMPLETE!', Colors.GREEN)
                    
                    break
            except FileNotFoundError:
                log(persona, 'Meeting file was deleted or moved.', Colors.RED)
                sys.exit(1)
            
            time.sleep(POLL_INTERVAL_SECONDS)
        
        # File changed or timeout - output meeting content
        print()
        log(persona, 'File change detected! Reading new content...', Colors.GREEN)
        print_separator()
        
        with open(meeting_file, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        status = extract_status(new_content)
        if status:
            color = Colors.YELLOW if status == 'COMPLETE' else Colors.GREEN
            print(f'{color}Current Status: {status}{Colors.RESET}')
            print()
        
        messages = extract_messages(new_content)
        display_messages(messages, context_messages)
        
        print_separator()
        log(persona, 'Review the content above and respond if appropriate.', Colors.GREEN)
        log(persona, 'To respond: Run script again with --message parameter', Colors.YELLOW)
        log(persona, 'If Status is COMPLETE, do not restart monitoring.', Colors.YELLOW)
        
    except Exception as e:
        log(persona, f'Error monitoring file: {e}', Colors.RED)
        sys.exit(1)
    
    log(persona, 'Script complete. Terminal will remain open for review.', Colors.GREEN)
    log(persona, 'You can manually close this terminal or it will be reused for the next command.', Colors.YELLOW)
    sys.exit(0)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Python script to manage meeting messages and monitor for changes',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--persona', '-p',
        required=True,
        help='Agent persona name (required)'
    )
    parser.add_argument(
        '--meeting-file', '-f',
        default='meetings/meeting.md',
        help='Meeting file path (default: meetings/meeting.md)'
    )
    parser.add_argument(
        '--message', '-m',
        help='Message to post to the meeting'
    )
    parser.add_argument(
        '--context-messages', '-c',
        type=int,
        default=5,
        help='Number of recent messages to display (default: 5)'
    )
    parser.add_argument(
        '--end-meeting', '-e',
        action='store_true',
        help='Flag to end the meeting (sets Status to COMPLETE)'
    )
    parser.add_argument(
        '--fetch',
        action='store_true',
        help='Fetch current content without monitoring'
    )
    
    return parser.parse_args()

def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    # Validate meeting file exists
    if not os.path.exists(args.meeting_file):
        log(args.persona, f'ERROR: Meeting file not found: {args.meeting_file}', Colors.RED)
        log(args.persona, 'Please ensure the meeting file exists before starting the watch.', Colors.YELLOW)
        sys.exit(1)
    
    # Handle different operation modes
    if args.end_meeting:
        end_meeting(args.persona, args.meeting_file)
        return
    
    if args.message:
        post_message(args.persona, args.meeting_file, args.message)
    
    if args.fetch:
        fetch_content(args.persona, args.meeting_file, args.context_messages)
        return
    
    # Default: monitor for changes
    monitor_file(args.persona, args.meeting_file, args.context_messages)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Colors.YELLOW}Interrupted by user{Colors.RESET}')
        sys.exit(130)
    except Exception as e:
        print(f'{Colors.RED}Fatal error: {e}{Colors.RESET}', file=sys.stderr)
        sys.exit(1)
