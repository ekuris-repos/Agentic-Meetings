# Meeting: VS Code Extension - Architecture & Implementation Plan

**Status:** COMPLETE  
**Date:** October 21, 2025  
**Participants:** @Backend-Architect, @Frontend-Developer, @Tech-Lead, @Product-Manager, @DevOps-Engineer

## Meeting Objective

Design and plan the implementation of a VS Code extension that transforms our current PowerShell-based multi-agent meeting system into a production-ready extension with a rich UI, automatic agent coordination, and marketplace distribution.

## Topics for Discussion

1. Core extension architecture - file structure, key components, VS Code API usage
2. Agent execution strategy - Chat Participants API vs Language Model API
3. UI/UX design - sidebar tree view, webview meeting panel, status bar integration
4. Migration path - what to keep from current PowerShell implementation, what to rebuild in TypeScript
5. MVP feature prioritization - what ships in v1.0, what comes later
6. Development timeline and task breakdown

## Outcomes

**Topic 1 - Core extension architecture:**  
- Feature-based folder structure: `src/agents/`, `src/meeting/`, `src/ui/`, `src/infra/` (not technical layers)
- Centralized state management: extension-host controller using workspaceMemento + durable JSON log
- Event-driven architecture: typed events for UI and automation consumers
- Shared infrastructure layer for cross-cutting concerns (persistence, API clients, telemetry)

**Topic 2 - Agent execution strategy:**  
- Use Chat Participants API (not Language Model API directly)
- Benefits: Multi-agent turn management, built-in UI integration, native conversation views
- Reduces custom scheduling logic and integrates with VS Code conversation rendering
- Allows persisting conversation handles in state controller for workflow orchestration

**Topic 3 - UI/UX design:**  
- Sidebar tree view: Groups meetings by workspace and status with active agent badges
- Webview panel: Dedicated transcript view with avatars, timeline controls, and inline actions
- Status bar: Shows active meeting count + current speaking agent; click to navigate to transcript
- Event-driven updates: Conversation status events update UI without polling

**Topic 4 - Migration path:**  
- Keep: Meeting protocol logic (proven), meeting-instructions.md as resource file
- Rebuild: PowerShell watch script → TypeScript agents, file-based storage → extension storage, UI from scratch
- Migration strategy: Phased approach with feature flag (PowerShell legacy mode → extension mode)
- Protocol porting: Migrate as JSON schemas, convert coordination to TypeScript state machine
- Sunset PowerShell after extension proves stable in beta testing

**Topic 5 - MVP feature prioritization:**  

**v1.0 Must-Have Features:**
- Sidebar tree view with meeting grouping by workspace/status and active agent badges
- Live transcript webview panel with avatars, timeline controls, and inline actions
- Status bar integration (active meeting count + current speaker, click to navigate)
- Chat Participants API integration for agent orchestration
- Persisted state management (workspaceMemento + JSON log)
- Feature flag system for PowerShell-to-extension migration
- CI/CD pipeline with VSIX packaging
- Basic telemetry for error tracking
- Automated testing (unit tests for protocol logic, integration tests for Chat Participants API)

**Deferred to v1.1+:**
- Marketplace auto-update functionality
- Advanced analytics and reporting
- Collaborative editing controls
- Deep theming customization

**Topic 6 - Development timeline and task breakdown:**  

**Timeline: 12-week sprint (3 phases)**

**Phase 1 - Foundation (Weeks 1-4):**
- Extension skeleton and project setup
- State management infrastructure (workspaceMemento + JSON log)
- CI/CD pipeline with VSIX packaging
- Test infrastructure setup
- Lock backend event schema by Week 3
- Quality Gate: Working CI/CD with basic tests

**Phase 2 - Implementation (Weeks 5-8):**
- Backend: Event schema delivery (Week 5), Chat Participants API integration, persistence layer
- Frontend: Sidebar tree view, webview transcript panel, status bar (parallel work after event schema)
- File watching service (TypeScript migration from PowerShell)
- Quality Gate: >70% integration test coverage

**Phase 3 - Refinement (Weeks 9-12):**
- Load testing and orchestration engine validation (Week 9)
- Feature flag system for migration
- Marketplace preparation
- Beta user validation
- Quality Gate: Successful beta validation before marketplace launch

**Parallel Work Streams:**
- Backend and Frontend can work in parallel starting Week 5 (after event schema is locked)
- DevOps CI/CD setup enables continuous testing throughout Phases 2-3

## Transcript

**[Product-Manager - 2025-10-21 11:07:12]:** Welcome everyone! I've reviewed the objectives - we're transforming our PowerShell meeting system into a production-ready VS Code extension. Let's start with Topic 1: Core extension architecture. @Tech-Lead, what's your recommended approach for the project structure and key components?

**[Backend-Architect - 2025-10-21 11:07:52]:** Joining to cover backend architecture considerations.

**[Frontend-Developer - 2025-10-21 11:08:02]:** I'm joining to cover frontend architecture and UI considerations for the extension.

**[Product-Manager - 2025-10-21 11:08:07]:** Welcome @Backend-Architect! While we wait for @Tech-Lead, what are your initial thoughts on how the extension should handle agent state and coordination?

**[Tech-Lead - 2025-10-21 11:08:45]:** Joining to address technical architecture and guide our design decisions. @Product-Manager, I'll tackle your question on core architecture first.

For **Topic 1 - Core extension architecture**, I recommend this structure:

```typescript
// Directory structure:
extension-root/
├── src/
│   ├── extension.ts           # Entry point, API registration
│   ├── agents/
│   │   ├── agent-registry.ts  # Agent lifecycle, state management
│   │   ├── agent-types.ts     # Interfaces & types
│   │   └── chat-participant.ts # Chat Participants API handler
│   ├── meeting/
│   │   ├── meeting-manager.ts # Meeting coordination logic
│   │   ├── meeting-store.ts   # Meeting state persistence
│   │   └── protocol.ts        # Meeting protocol implementation
│   ├── ui/
│   │   ├── webview/
│   │   │   ├── meeting-panel.ts
│   │   │   └── styles/
│   │   └── sidebar/
│   │       └── tree-provider.ts
│   └── utils/
├── package.json
├── tsconfig.json
└── esbuild.config.js
```

**Key architectural principles:**

1. **Agent Registry Pattern** - Centralized agent lifecycle management with spawn/terminate hooks
2. **Meeting State Machine** - Enforce protocol through defined states (IDLE → ACTIVE → COMPLETE)
3. **Separation of Concerns** - Keep meeting protocol, agent execution, and UI independent
4. **VS Code API as Infrastructure** - Use VS Code as the runtime (workspace storage, output channels, webviews)

Should we discuss how @Backend-Architect sees this fitting with your coordination concerns?

**[Backend-Architect - 2025-10-21 11:08:56]:** I recommend centralizing agent state in an extension-host controller that persists via workspaceMemento plus a durable JSON log and emits typed events for UI and automation consumersdoes that match the durability we need?

**[Product-Manager - 2025-10-21 11:09:04]:** @Backend-Architect that approach sounds solid for durability and observability. @Tech-Lead, does that align with your vision for the core architecture?

**[Frontend-Developer - 2025-10-21 11:09:13]:** Centralizing state with a durable log works well for the meeting UI because the webview can always rebuild the context from a single source.

**[Tech-Lead - 2025-10-21 11:09:20]:** @Backend-Architect, your approach aligns perfectly - workspaceMemento for fast state recovery combined with a durable JSON log gives us both performance and auditability.

**[Product-Manager - 2025-10-21 11:09:28]:** Great alignment on state management. @Tech-Lead, what about the overall folder structure - src/controllers, src/views, src/models? How should we organize the codebase?

**[Tech-Lead - 2025-10-21 11:10:05]:** I'd recommend organizing by domain features (agents/, meeting/, ui/) rather than technical layersthis keeps related concerns together and scales better as we add features.

**[Frontend-Developer - 2025-10-21 11:10:14]:** Grouping by feature domains also helps the UI layer because each webview module can bundle its assets with the related meeting workflows.

**[Backend-Architect - 2025-10-21 11:10:16]:** Feature directories work well if we also carve out an infra layer for shared persistence, API clients, and telemetry helpers to keep cross-cutting code consistent.

**[Product-Manager - 2025-10-21 11:10:25]:** @Frontend-Developer, does domain-based organization (agents/, meeting/, ui/) work well for the webview components you'll be building?

**[Tech-Lead - 2025-10-21 11:10:32]:** @Backend-Architect, absolutelylet's add src/infra/ for shared utilities, and keep each feature domain responsible for its own domain logic.

**[Frontend-Developer - 2025-10-21 11:10:43]:** Yes, domain-based directories let each webview ship its data adapters, state hooks, and styles together so the UI stays cohesive and maintainable.

**[Product-Manager - 2025-10-21 11:11:22]:** Topic 1 documented! Moving to Topic 2: Agent execution strategy. Should we use Chat Participants API or Language Model API for running agent conversations?

**[Tech-Lead - 2025-10-21 11:11:28]:** Chat Participants API is the right choiceit's purpose-built for multi-agent scenarios, has built-in UI integration, and supports structured conversations better than the lower-level LM API.

**[Backend-Architect - 2025-10-21 11:11:34]:** For predictable orchestration I favor the Chat Participants API because it handles multi-agent turn management, lets us persist conversation handles in our state controller, and reduces custom scheduling logic.

**[Product-Manager - 2025-10-21 11:11:35]:** @Backend-Architect, does Chat Participants API give us enough control for coordinating multi-agent workflows, or do we need the Language Model API for finer control?

**[Frontend-Developer - 2025-10-21 11:11:45]:** Chat Participants API also feeds the VS Code conversation view so we can sync our webview timeline with native renderers without duplicating transcript logic.

**[Backend-Architect - 2025-10-21 11:11:48]:** Participants gives us fine-grained control through custom turn policies, system prompts, and ability to inject responses while still letting us invoke the Language Model API on the side for bespoke tools when a workflow needs it.

**[Tech-Lead - 2025-10-21 11:11:51]:** Chat Participants API provides sufficient control through response transformationwe define agent behaviors in chat-participant.ts handlers and use the core meeting protocol for orchestration logic.

**[Product-Manager - 2025-10-21 11:12:10]:** Topic 2 documented! Now for Topic 3: UI/UX design. @Frontend-Developer, what's your vision for the user interface - sidebar, webview panels, status bar?

**[Frontend-Developer - 2025-10-21 11:12:14]:** Participants also emits conversation status events we can reflect in the status bar so users see which agents are active without polling.

**[Product-Manager - 2025-10-21 11:12:21]:** @Frontend-Developer, specifically - should we have a tree view in the sidebar showing active meetings, a webview panel for the meeting transcript, or both?

**[Frontend-Developer - 2025-10-21 11:12:33]:** We should ship a sidebar tree that groups meetings by workspace and status with badges indicating active agents.

**[Product-Manager - 2025-10-21 11:12:40]:** And what about the meeting transcript view - should that be a webview panel or use the native VS Code conversation UI?

**[Frontend-Developer - 2025-10-21 11:12:55]:** Let's host the transcript in a dedicated webview panel so we can render avatars, timeline controls, and quick actions inline.

**[Product-Manager - 2025-10-21 11:13:02]:** @Tech-Lead, for the status bar - what information should we display there? Active meeting count, agent status, something else?

**[Tech-Lead - 2025-10-21 11:13:08]:** Status bar should show active meeting count plus current agent speakingthat's glanceable context without cluttering the UI, and clicking it navigates to the transcript panel.

**[Backend-Architect - 2025-10-21 11:13:27]:** For the status bar we can stream summary events from the state controller so the UI updates push-style without each meeting view polling for agent activity.

**[Frontend-Developer - 2025-10-21 11:13:29]:** We can pulse the status bar item while an agent is speaking so users know when to open the transcript.

**[Product-Manager - 2025-10-21 11:13:30]:** Topic 3 documented! Moving to Topic 4: Migration path. What should we keep from the current PowerShell implementation and what needs to be rebuilt in TypeScript?

**[DevOps-Engineer - 2025-10-21 11:13:47]:** Joining to address deployment, CI/CD pipeline setup, and migration considerations from an operational perspective.

**[Tech-Lead - 2025-10-21 11:13:54]:** Keep the meeting protocol logic (it's proven)rewrite the PowerShell watch script into TypeScript agents, the state persistence in extension storage, and the UI from scratch for the webview panel.

**[Product-Manager - 2025-10-21 11:13:55]:** Welcome @DevOps-Engineer! Your timing is perfect. @Tech-Lead, what's your view on the migration - can we port the meeting protocol directly or does it need redesign?

**[Backend-Architect - 2025-10-21 11:13:58]:** We should migrate the meeting protocol definitions and transcripts as JSON schemas while rewriting all orchestration logic in TypeScript so the extension owns scheduling, storage, and integrations.

**[Tech-Lead - 2025-10-21 11:14:01]:** The protocol logic can be ported directly with minimal redesignwe just move it from PowerShell coordination into a TypeScript state machine that Chat Participants API triggers.

**[DevOps-Engineer - 2025-10-21 11:14:03]:** From a deployment perspective, we should preserve the meeting-instructions.md protocol as a resource file and establish a CI/CD pipeline early for automated packaging and marketplace publishing.

**[Product-Manager - 2025-10-21 11:14:05]:** @DevOps-Engineer, should we maintain backward compatibility with the PowerShell system during migration, or make a clean break?

**[DevOps-Engineer - 2025-10-21 11:14:12]:** I recommend a phased migration: keep PowerShell scripts operational initially, add a feature flag to toggle between legacy and extension modes, then sunset PowerShell once the extension proves stable in beta testing.

**[Frontend-Developer - 2025-10-21 11:14:17]:** We should keep the markdown meeting templates and protocol docs so the extension UI can render them without content rewrites.

**[Tech-Lead - 2025-10-21 11:14:18]:** @DevOps-Engineer, phased migration is the right callfeature flags lower risk and we can gather real-world feedback on the extension before retiring PowerShell tooling.

**[Backend-Architect - 2025-10-21 11:14:21]:** During the phased migration we should keep transcript storage compatible by letting both PowerShell and the extension read/write the same JSON format behind a feature-flagged gateway.

**[Frontend-Developer - 2025-10-21 11:14:29]:** We should rebuild the PowerShell watcher as a TypeScript file-watcher service that streams updates into the webview through VS Code messaging APIs.

**[DevOps-Engineer - 2025-10-21 11:14:37]:** We should add telemetry hooks during migration to compare PowerShell vs extension performance and track adoption rates across the feature flag boundary.

**[Backend-Architect - 2025-10-21 11:14:56]:** Telemetry comparisons will be simpler if we emit structured events from the infra layer so both PowerShell and extension clients feed the same ingestion pipeline.

**[Product-Manager - 2025-10-21 11:14:57]:** Topic 4 documented! Now Topic 5: MVP prioritization. From a product perspective, what features are must-haves for v1.0 versus nice-to-haves for later releases?

**[Backend-Architect - 2025-10-21 11:15:08]:** For v1 we must ship reliable agent orchestration with persisted transcripts, feature-flagged migration support, and telemetry instrumentation while deferring marketplace auto-updates and advanced analytics to later iterations.

**[Tech-Lead - 2025-10-21 11:15:15]:** For v1.0 MVP, we need: extension activation with meeting sidebar, webview transcript panel, Chat Participants integration, and basic file watchingdefer advanced features like marketplace publishing until v1.1.

**[Product-Manager - 2025-10-21 11:15:16]:** @Frontend-Developer, for v1.0 UI - do we need the full webview panel, or can we start with just sidebar tree view and status bar?

**[DevOps-Engineer - 2025-10-21 11:15:17]:** For v1.0 MVP, I prioritize: automated CI/CD pipeline with VSIX packaging, basic telemetry for error tracking, and a manual marketplace publishing workflow.

**[Frontend-Developer - 2025-10-21 11:15:25]:** For v1 we need the sidebar tree, live transcript webview, and status bar pulse while collaborative editing controls and deep theming can wait for later.

**[DevOps-Engineer - 2025-10-21 11:15:32]:** We should also include automated testing in v1.0 CI pipeline - at minimum unit tests for core orchestration and integration tests for the Chat Participants API.

**[Product-Manager - 2025-10-21 11:15:33]:** So for v1.0 MVP: sidebar tree, webview transcript, status bar, Chat Participants integration, persisted state, feature flag for migration, CI/CD pipeline, and basic telemetry. Defer marketplace automation and advanced analytics to v1.1+. Does everyone agree?

**[DevOps-Engineer - 2025-10-21 11:15:40]:** Agreed on v1.0 scope - that gives us a deployable, testable foundation while keeping the initial release focused and shippable.

**[Frontend-Developer - 2025-10-21 11:15:45]:** We need the webview in v1 because transcript actions and agent controls won't fit cleanly inside the tree view alone.

**[Tech-Lead - 2025-10-21 11:15:54]:** @DevOps-Engineer, exactlyautomated testing is non-negotiable for extension stability; we need unit tests for protocol logic and integration tests for API integration from day one.

**[Frontend-Developer - 2025-10-21 11:16:03]:** Agreed on the v1 scope because it delivers the essential UI surfaces without overextending the first release.

**[Backend-Architect - 2025-10-21 11:16:05]:** Agreedthe v1 package needs reliable state persistence, participant orchestration, and observability so we can scale to automation later.

**[Product-Manager - 2025-10-21 11:17:23]:** Topic 5 documented! Final topic - Topic 6: Development timeline and task breakdown. @Tech-Lead, how should we break down the work and what's a realistic timeline for v1.0?

**[DevOps-Engineer - 2025-10-21 11:17:32]:** From a release perspective, we need: Week 1-2 CI/CD setup and test infrastructure, Week 3-6 parallel development tracks, Week 7 integration testing, Week 8 beta deployment and marketplace submission prep.

**[Tech-Lead - 2025-10-21 11:17:32]:** I suggest a 12-week sprint split into 3 phases: Phase 1 (Weeks 1-4) foundationextension skeleton, state management, CI/CD setup; Phase 2 (Weeks 5-8) implementationChat Participants agents, webview, file watching; Phase 3 (Weeks 9-12) refinementtesting, migration flags, marketplace prep.

**[Product-Manager - 2025-10-21 11:17:39]:** @Backend-Architect and @Frontend-Developer, can you work in parallel during Phase 2? What are the dependencies between your work streams?

**[Frontend-Developer - 2025-10-21 11:20:15]:** Once the backend locks the typed meeting event schema at the end of Phase 1 we can build the webview and sidebar in parallel without blocking.

**[Backend-Architect - 2025-10-21 11:20:33]:** YesPhase 2 backend will deliver the event schema and state controller first week so frontend can consume typed events while we wire Chat Participants and persistence.

**[Product-Manager - 2025-10-21 11:20:42]:** So we have a 12-week timeline: Weeks 1-4 foundation, Weeks 5-8 parallel implementation, Weeks 9-12 refinement and marketplace prep. Does this timeline feel realistic to everyone?

**[Tech-Lead - 2025-10-21 11:20:48]:** The 12-week timeline is realistic with this phased approach and clear dependencieswe ship a production-ready v1.0 without over-committing.

**[DevOps-Engineer - 2025-10-21 11:20:50]:** We should define quality gates at each phase boundary: Phase 1 must have working CI/CD with basic tests, Phase 2 requires integration test coverage >70%, Phase 3 needs successful beta user validation before marketplace launch.

**[Backend-Architect - 2025-10-21 11:20:51]:** Timeline is achievable if we lock backend schema decisions by Week 3 and reserve Week 9 for load testing the orchestration engine.

**[Frontend-Developer - 2025-10-21 11:21:15]:** The 12-week schedule works for frontend because it gives us four weeks to finalize event contracts, four weeks for UI buildout, and four weeks for polish and marketplace readiness.

**[Product-Manager - 2025-10-21 11:21:43]:** All six topics are now documented with outcomes! Before we close, does anyone have remaining concerns or questions about the architecture, timeline, or MVP scope?

**[DevOps-Engineer - 2025-10-21 11:21:51]:** No concerns from the deployment and operations side - we have clear quality gates, testable milestones, and a practical phased rollout strategy.

**[Backend-Architect - 2025-10-21 11:22:01]:** No further concernsbackend next steps are codifying the meeting state machine and event schema ahead of Phase 2 handoff.

**[Frontend-Developer - 2025-10-21 11:22:07]:** No concerns from frontendwe have clear UI milestones and dependencies lined up across the phases.

**[Tech-Lead - 2025-10-21 11:23:18]:** No concerns from technical leadershipwe have a solid architecture, realistic timeline with clear dependencies, and quality gates at every phase boundary. I'm confident this team can deliver v1.0.
