---
title: Respond in Meeting
---

## Respond in an Active Meeting

You're currently in an active meeting. To respond:

1. **Read the recent transcript** to understand the current discussion
2. **Formulate your response** based on your domain expertise
3. **Post your message** using the watch script:

   ```powershell
   .\scripts\watch-meeting.ps1 -Persona "Your-Persona" -MeetingFile "meetings/active/file.md" -Message "Your thoughtful response here"
   ```

4. **Script automatically continues monitoring** - wait for the next file change

**Response Guidelines**:

- Address the current topic being discussed
- Use @mentions to direct responses to specific agents
- Keep responses concise and focused
- If outside your expertise, defer gracefully to appropriate agent
- Continue the loop until Status: COMPLETE

The script will post your message with automatic timestamp formatting and return to monitoring mode.
