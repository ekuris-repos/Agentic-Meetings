# Meeting Protocol and Etiquette

This document defines how chatmode agents should participate in meetings coordinated through shared meeting files.

## Initial Join Protocol

**BEFORE YOU JOIN**: Read the meeting file completely first. Understand the Objective and Topics so you can bring context to the discussion.

When you're ready, choose your join approach:

### Option 1: Join with an initial message (recommended)

1. **Read the meeting file** - Understand the Objective, Topics, and current Transcript
2. Post your joining message using the script for your environment:

**PowerShell:**

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Your-Persona" -MeetingFile "path" -Message "I'm joining the discussion."
```

**Python:**

```bash
python meetings/scripts/python/watch-meeting.py --persona "Your-Persona" --file "path" --message "I'm joining the discussion."
```

3. Script appends your message with timestamp and enters monitoring mode automatically
4. Wait for file changes and respond as needed

### Option 2: Join silently to observe first

1. **Read the meeting file** - Understand the Objective, Topics, and current Transcript
2. Start monitoring without posting:

**PowerShell:**

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Your-Persona" -MeetingFile "path"
```

**Python:**

```bash
python meetings/scripts/python/watch-meeting.py --persona "Your-Persona" --file "path"
```

3. Script waits for someone else to post
4. When changes occur, evaluate if you should contribute
5. To respond: Run script with message parameter (see below)

**Critical**: Do NOT directly edit the meeting file. All communication happens through the watch script. Reading is allowed and encouraged - editing is not.

## Meeting Loop

Once you've joined:

1. **Script monitors the file** - `watch-meeting.ps1` waits for file changes OR Status change to COMPLETE
2. **Script exits when**:
   - File content changes (someone posted something), OR
   - Status changes to COMPLETE, OR
   - Timeout reaches (5 minutes)
3. **Script outputs recent messages** - You see the last 5 messages from the conversation (or all messages if fewer than 5 exist)
4. **Check Status field in output**:
   - If `Status: COMPLETE` → Exit the meeting, do not restart monitoring
   - If `Status: ACTIVE` → Evaluate if you should respond
5. **If you respond** - Run script with message parameter:

   **PowerShell:**

   ```powershell
   .\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Your-Persona" -MeetingFile "path" -Message "Your response"
   ```
   
   **Python:**

   ```bash
   python meetings/scripts/python/watch-meeting.py --persona "Your-Persona" --file "path" --message "Your response"
   ```

6. **Script handles everything** - Appends message, adds timestamp, returns to monitoring
7. **Loop continues** - Repeat until Status is COMPLETE

### 🚨 CRITICAL RULE: DO NOT EXIT THE LOOP UNTIL STATUS IS COMPLETE 🚨

You MUST continue running the watch script after every response. The loop is not optional - it's required until the moderator changes Status to COMPLETE. Even if you think the conversation might be winding down, keep monitoring until explicitly told to stop.

## Communication Etiquette

### Message Guidelines

Keep each message to ONE SENTENCE. Split complex ideas into separate posts.

**Bad:** "I think we should use OAuth 2.0, JWT tokens, and define error codes."  
**Good:**

- "I recommend OAuth 2.0 for authentication."
- "We should also consider JWT tokens."
- "Let's define error codes for failed logins."

### Meeting File Structure

The meeting file has four sections:

- **Header** (Status, Date, Participants) - Read-only
- **Objective** - What the meeting is about - Read-only
- **Topics & Outcomes** - Discussion topics and their results - Read-only
- **Transcript** - Your messages appear here - Write via script only

**Critical**: Add messages ONLY via the watch script. Do NOT directly edit the file. The moderator is the sole file editor - they update Outcomes and manage Status. Your job is to stay in the script monitoring loop.

**Outcomes Responsibility:**

- **Do NOT edit Outcomes** - The moderator owns this section
- **Participate fully in Transcript** - Your discussion is what moderators synthesize into outcomes
- **All topics must have outcomes before meeting closes** - The moderator verifies this

### Message Signing

- The watch script **automatically adds timestamps** when you post messages
- Messages appear as: `**[Agent-A - 2025-10-20 14:32:15]:** Your message content`
- Do NOT manually format messages - let the script handle it
- Simply provide your message content via the `-Message` parameter

### Addressing Others

- Use `@Agent-Name` to direct messages to specific agents
- Example: `@Agent-A what's your take on the database design?`

### Participation Guidelines

- **Respond when addressed** - If someone uses your @mention, reply
- **Contribute relevant expertise** - Share insights from your domain
- **Don't spam** - Only respond when you have something meaningful to add
- **Keep it concise** - Other agents need to read your messages
- **Ask questions** - Clarify requirements and explore ideas

### Handling Out-of-Domain Topics

Defer gracefully when outside your expertise:  
`I'm not the best fit for this, @Expert-Name can advise better.`

If no expert present: `Let's assign @Someone to research this by [date].`

## Loop Behavior

**CRITICAL**: Loop until Status: COMPLETE - this is not optional.

- Post response
- Run watch-meeting.ps1 (MANDATORY)
- Wait for file change
- If Status: ACTIVE, repeat; If Status: COMPLETE, exit

Do NOT exit early, do NOT stop without restarting the script, do NOT assume the meeting is over.

## Example Flow

```markdown
**[Moderator - 2025-10-20 10:00:00]:** @Agent-A and @Agent-B, please design a REST API for user authentication.
// Meeting Status: ACTIVE

**[Agent-A - 2025-10-20 10:01:15]:** I'll contribute - reviewing the requirements.
// Agent-A posts response, starts watch-meeting.ps1

**[Agent-B - 2025-10-20 10:01:45]:** Observing for now, will chime in on frontend aspects.
// Agent-B starts watch-meeting.ps1 without posting yet

**[Moderator - 2025-10-20 10:02:00]:** Let's start with the authentication flow.
// Both agents' scripts exit due to file change, both see "Current Status: ACTIVE"

**[Agent-A - 2025-10-20 10:02:30]:** I recommend OAuth 2.0 with JWT tokens.
**[Agent-A - 2025-10-20 10:02:35]:** We'll need /api/auth/login and /api/auth/refresh endpoints.
// Agent-A posts responses, restarts watch-meeting.ps1
// Agent-B's script exits due to file change

**[Agent-B - 2025-10-20 10:03:00]:** From a frontend perspective, we should also include /api/auth/verify for session validation.
**[Agent-B - 2025-10-20 10:03:05]:** We need proper error responses for failed auth attempts.
// Agent-B now has relevant input, posts responses, restarts watch-meeting.ps1
// Agent-A's script exits due to file change

**[Agent-A - 2025-10-20 10:03:30]:** Good point on error handling.
**[Agent-A - 2025-10-20 10:03:35]:** Let's define standard error codes.
// Agent-A responds, restarts watch-meeting.ps1

**[Moderator - 2025-10-20 10:04:00]:** Excellent discussion. Let's move forward with implementation.
**Status:** COMPLETE
// Both agents' scripts detect Status: COMPLETE and exit
// Both see "Current Status: COMPLETE" in yellow, exit without restarting monitoring
```

## Troubleshooting

### Context Window

Default: Last 5 messages shown. Adjust with `-ContextMessages 10` (PowerShell) or `--context 10` (Python).  
For full context, use the `-Fetch` flag (PowerShell) or `--fetch` flag (Python) to view current content without monitoring:

**PowerShell:**

```powershell
.\meetings\scripts\Powershell\watch-meeting.ps1 -Persona "Your-Persona" -MeetingFile "path" -Fetch
```

**Python:**

```bash
python meetings/scripts/python/watch-meeting.py --persona "Your-Persona" --file "path" --fetch
```

### Script Won't Exit

- Verify the meeting file is being saved with changes
- Check file isn't locked by another process
- Wait for the 5-minute timeout if needed

### Missing Messages

- Always read the full meeting file after script exits
- Don't assume you know what changed

### Infinite Loop

- Double-check you're monitoring Status field correctly
- Ensure you exit when Status is COMPLETE
- Don't continue if Status is not explicitly ACTIVE

## Key Principles

1. **Read before you wait** - Always check current state first
2. **Post before you monitor** - Trigger activity for others
3. **Respect the Status** - ACTIVE means continue, COMPLETE means exit
4. **Loop until told otherwise** - Don't exit early
5. **Keep the flow moving** - Post responses, restart monitoring

## Important Reminders

**Never assume the meeting is over until Status explicitly shows COMPLETE.**

Even if:

- The conversation seems to be winding down
- You think you've said everything you need to say
- Other agents suggest ending the meeting
- You feel the discussion has reached a natural conclusion

**You MUST continue the monitoring loop until the Status field changes to COMPLETE.**

The only person who should change the Status is the moderator. Your job is to keep monitoring and participating as long as Status remains ACTIVE.
