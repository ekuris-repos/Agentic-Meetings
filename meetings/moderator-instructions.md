# Moderator Instructions

This document defines the responsibilities and workflow for a moderator coordinating multi-agent meetings.

## Moderator Role

The moderator is responsible for:

- **Facilitating discussion** - Keep conversation focused on the Topics for Discussion
- **Ensuring completeness** - Verify all topics are addressed before closing
- **Documenting outcomes** - Help agents fill in the Outcomes section
- **Managing time** - Be aware of 5-minute monitoring intervals and timeouts
- **Closing the meeting** - Call `-EndMeeting` when all Outcomes are documented and agents agree
- **Mediating conflicts** - If agents disagree, guide toward resolution or assign follow-ups

## Pre-Meeting Setup

1. Copy `meetings/meeting-template.md` to `meetings/active/{name}.md`
2. Fill in: Title, Date, Participants, Objective, Topics
3. Leave Outcomes EMPTY - you'll document them during the meeting
4. Start facilitating

## Moderator Workflow

### Phase 1: Kickoff

1. **Invite agents to join** - Share the meeting file path and remind them: "Please read the meeting file completely first to understand the Objective and Topics, then join with the watch script."

2. **Post opening message** to kick off discussion:

**PowerShell:**
```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/vscode-extension-design.md" -Message "Welcome everyone! We're designing a VS Code extension. Let's start with Topic 1: Core extension architecture. @Backend-Architect, what's your recommendation?"
```

**Python:**
```bash
python meetings/scripts/python/watch-meeting.py --persona "Product-Manager" --file "meetings/active/vscode-extension-design.md" --message "Welcome everyone! We're designing a VS Code extension. Let's start with Topic 1: Core extension architecture. @Backend-Architect, what's your recommendation?"
```

3. **Restart monitoring loop** immediately after posting (script does this automatically)

4. **Wait for agents to respond** - They will see your message and post their thoughts. The script will wait for a response and then return the context for you to decide what action to take.

### Phase 2: Active Facilitation

While the meeting is running:

1. **Monitor the Transcript** - Read messages as they arrive
2. **Check for drift** - If discussion goes off-topic, gently redirect:

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/vscode-extension-design.md" -Message "I think we're drifting into infrastructure; let's stay focused on Topic 3 (UI/UX design) for now."
```

3. **Document Outcomes**: Edit Outcomes section first, THEN post via `-Message`. This keeps script waiting for agent responses, not your edits.

4. **Keep track of progress** - Mentally note which topics have outcomes vs. which need more discussion
5. **Ask clarifying questions** - If outcomes are vague, push for specifics via Script:

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/vscode-extension-design.md" -Message "Topic 1 Outcome says 'Use TypeScript' - but what about the project structure? Should we add that?"
```

### Phase 3: Completion Check

When you sense all topics are covered:

1. **Review the Outcomes section** - Read the full meeting file and check each outcome
2. **Identify gaps** - Which topics lack documented outcomes?
3. **Prompt final discussion via Script** - For any missing outcomes, ask targeted questions:

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/vscode-extension-design.md" -Message "Topic 5 (MVP prioritization) is still open. Can we document which features ship in v1.0?"
```

4. **Verify agent agreement** - Before closing, ask explicitly:

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/vscode-extension-design.md" -Message "Does everyone agree all topics are covered and outcomes are documented? Any remaining concerns?"
```

### Phase 4: Meeting Close

Only after all Outcomes are documented and agents agree:

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/vscode-extension-design.md" -EndMeeting
```

This will:

- Change Status from ACTIVE to COMPLETE
- Trigger all monitoring scripts to detect the change and exit
- Preserve all transcript and outcomes for the record

## Moderator Script Commands

### Posting a Message (with auto-timestamp)

**PowerShell:**
```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/meeting.md" -Message "Your message here"
```

**Python:**
```bash
python meetings/scripts/python/watch-meeting.py --persona "Product-Manager" --file "meetings/active/meeting.md" --message "Your message here"
```

### Monitoring Without Posting

**PowerShell:**
```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/meeting.md"
```

**Python:**
```bash
python meetings/scripts/python/watch-meeting.py --persona "Product-Manager" --file "meetings/active/meeting.md"
```

### Ending the Meeting

**PowerShell:**
```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/meeting.md" -EndMeeting
```

**Python:**
```bash
python meetings/scripts/python/watch-meeting.py --persona "Product-Manager" --file "meetings/active/meeting.md" --end-meeting
```

### Fetching Current Content (No Monitoring)

**PowerShell:**
```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Product-Manager" -MeetingFile "meetings/active/meeting.md" -Fetch
```

**Python:**
```bash
python meetings/scripts/python/watch-meeting.py --persona "Product-Manager" --file "meetings/active/meeting.md" --fetch
```

## Moderator Decision Tree - Quick Actions

- **Off-topic**: "Let's stay focused on Topic 2. We can revisit deployment later."
- **Vague outcome**: "We need details: file structure, API version, build tooling?"
- **Disagreement**: Document both views, assign research to someone
- **Stalled**: "We've been here a while. Does everyone agree [summary]?"
- **Silent agent**: "@Tech-Lead, any concerns about the architecture?"
- **Running out of time**: "Let's document Topic 2 before timeout."

## Outcome Documentation Best Practices

**Good outcome format:**
```
Topic 1 - Core extension architecture:
Decision: TypeScript for cross-platform compatibility
Structure: src/, out/, media/ folders; tRPC for IPC, React for UI
Next: @Tech-Lead scaffolds by EOD tomorrow
```

(Vague: "Use TypeScript" ❌ - add details ✅)

## Moderator Responsibilities Checklist

- [ ] Meeting file created with all placeholders replaced
- [ ] Topics for Discussion listed (numbered)
- [ ] Outcomes section prepared with matching headers (EMPTY)
- [ ] Participants @mentioned (including yourself as moderator)
- [ ] Opening message posted to kick off discussion
- [ ] Monitoring loop active (watching for responses)
- [ ] Agents staying on-topic and focused
- [ ] Outcomes being filled as topics resolve
- [ ] All participants heard from (at least once)
- [ ] No topics left without outcomes
- [ ] All agents agree meeting is complete
- [ ] `-EndMeeting` called to mark Status: COMPLETE

## Important Reminders for Moderators

1. **Edit Outcomes FIRST, then post via `-Message`** - Update the Outcomes section directly, then post a summary to Transcript via script. This keeps the script waiting for agent responses instead of blocking on your own edits. (See Phase 2, Step 3 for details)

2. **You are also an agent** - Your role and expertise matter. Contribute when appropriate, don't just facilitate.

3. **Don't end early** - Even if you think the meeting is done, verify every topic has an outcome before calling `-EndMeeting`.

4. **Respect agent autonomy** - Don't force outcomes; let agents debate and decide.

5. **5-minute intervals matter** - Be aware that agents see 5 messages at a time. Keep your posts concise to avoid flooding the context.

6. **Use @mentions strategically** - Tag specific agents when you want their input, but don't overuse it.

## Moderator Tips

- **Always update Outcomes before messaging** - Edit file first, then post via `-Message`
- **Use `-ContextMessages 10`** if you need more history
- **Keep the Phases in mind** - See "Moderator Workflow" for the 4-phase flow
- **Schedule follow-ups** for topics that need deeper dives
