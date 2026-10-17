# Microscope AI

A local-first React prototype for running *Microscope* games with a mixed table of human and AI players.

## Run it

```bash
npm install
npm run dev
```

## What is implemented

- 2–5 configurable seats, each assigned to a human or a prompted AI persona
- A guided Lens-round turn rail based on the tabletop game loop
- A non-linear history board organized as History → Period → Event → Scene
- A card inspector with parent/child summaries and direct navigation
- Light/Dark tone display and an in-memory add-child interaction

This first slice deliberately keeps game state in React. The next architectural step is a durable event store plus an agent boundary that can retrieve the current Focus, Palette, ancestors, descendants, established facts, and relevant Legacies without giving the agent information or authority it should not have.
