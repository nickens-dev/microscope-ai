# Product direction

## Product principle

The app should facilitate Microscope, not play designer. It owns turn order, legal choices, context assembly, persistence, and navigation. Humans and agents own the history.

## Canonical game model

```text
Game
├── setup: big picture, starting/ending bookends, palette, first pass
├── players: ordered seats with human or agent controller
├── timeline
│   └── Period
│       └── Event
│           └── Scene
├── rounds: lens, focus, contributions, legacy
└── facts: statements established during play
```

Every history card has a tone, creator, created-at turn, summary, body, parent, ordered children, and provenance. Scenes additionally hold their Question, setting, required/banned characters, cast, role-play transcript, and answer.

## Agent boundary

An AI player should receive a role-specific context packet rather than the whole database:

1. The game premise, bookends, and Palette.
2. The current Focus, Lens, active step, and legal actions.
3. Its persona prompt and public table preferences.
4. The selected card's ancestors and immediate children.
5. Retrieved established facts and Legacies relevant to the proposed contribution.
6. A compact recent-turn transcript.

The agent proposes a typed action. The game engine validates it, shows it for review when configured, and only then commits it. Retrieval supports continuity; it must not turn previous cards into constraints that the rules do not impose.

## Next slices

1. Setup wizard and persisted games.
2. Typed turn-state machine with undo and an append-only action log.
3. Full card editor and chronological insertion/reordering.
4. Played Scene room with character assignment for both humans and agents.
5. Provider-neutral agent adapter, embeddings, retrieval inspection, and per-seat autonomy controls.
6. Export/import and shareable read-only histories.
