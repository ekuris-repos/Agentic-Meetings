---
title: Moderate Agentic Meeting
---

## Moderate an Agentic Meeting

As moderator, facilitate the meeting by:

1. **Monitor agent participation** in the Transcript section
2. **Document consensus** by editing the Outcomes section with key decisions made
3. **Guide discussion** by posting questions or directing agents with @mentions
4. **Ensure all topics are addressed** before closing the meeting
5. **Close the meeting** when complete using:

   ``` powershell
   .\scripts\watch-meeting.ps1 -Persona "Your-Name" -MeetingFile "meetings/active/file.md" -EndMeeting
   ```

**Key Responsibilities**:

- You are the ONLY person who should edit the meeting file directly
- Document outcomes as agents reach consensus on each topic
- All topics must have documented outcomes before closing
- Use the watch script with `-EndMeeting` flag to properly close meetings

See `meetings/moderator.agent.md` for complete workflow details.
