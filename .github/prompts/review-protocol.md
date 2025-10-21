---
title: Review Meeting Protocol
---

## Review Agentic Meeting Protocol

The protocol for participating in agentic meetings:

**Agent Participation Loop**:

1. Read the meeting file to understand context
2. Post messages via: `.\scripts\watch-meeting.ps1 -Persona "Your-Persona" -MeetingFile "path" -Message "your message"`
3. Script automatically enters monitoring mode
4. When file changes, evaluate and respond if appropriate
5. Continue loop until Status: COMPLETE

**Key Rules**:

- NEVER directly edit the meeting file (moderator only)
- ALWAYS continue monitoring until Status: COMPLETE
- Use @mentions to address specific agents
- Messages are automatically timestamped
- Read full protocol in `meetings/meeting-instructions.md`

**For Moderators**:

- Document outcomes in the Outcomes section
- Close meetings with `-EndMeeting` flag
- See `meetings/moderator-instructions.md` for details
