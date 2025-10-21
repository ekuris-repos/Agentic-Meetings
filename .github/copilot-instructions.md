# Agent Orchestration Test Workspace

This workspace is designed for testing multi-agent collaboration patterns using GitHub Copilot chatmodes with PowerShell-based coordination.

## Key Concepts

- **Chatmode Agents**: AI personas defined in `.github/chatmodes/` with minimal instructions
- **Meeting Coordination**: Shared `meetings/meeting.md` file for inter-agent communication
- **Meeting Protocol**: Centralized in `meetings/meeting-instructions.md` for all agents to follow
- **PowerShell Monitoring**: `scripts/watch-meeting.ps1` is a simple file watcher with no business logic
- **Protocol Loop**: Read → Post → Monitor → Wait → Check Status → Repeat until COMPLETE

## Development Guidelines

When working in this workspace:
- Agent personas should be minimal - they reference `meeting-instructions.md` for protocol details
- All meeting protocol logic lives in `meetings/meeting-instructions.md`, not in PowerShell scripts
- Agents sign messages with their persona identifier (e.g., `[Agent-A]:`)
- Use `@Agent-Name` to address specific agents in meeting files
- Follow the protocol: Read → Post joining message → Monitor → Respond → Loop until Status: COMPLETE
- PowerShell scripts are simple file watchers with no business logic