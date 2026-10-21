import { useMemo, useState } from 'react'
import { createGame } from "./api/games.js";

const seedCards = [
  { id: 'history', type: 'History', title: 'The empire learns to remember', summary: 'A civilization discovers that memory can be mined, traded, and weaponized.', tone: 'light', parent: null },
  { id: 'p1', type: 'Period', title: 'The age of private memory', summary: 'Memory belongs only to the person who lived it.', tone: 'light', parent: 'history' },
  { id: 'p2', type: 'Period', title: 'The Archive Ascendant', summary: 'A public archive becomes the heart of imperial power.', tone: 'dark', parent: 'history' },
  { id: 'p3', type: 'Period', title: 'The merciful forgetting', summary: 'The empire chooses which truths it can survive.', tone: 'light', parent: 'history' },
  { id: 'e1', type: 'Event', title: 'The first stolen childhood', summary: 'A magistrate proves a memory can be removed without killing its owner.', tone: 'dark', parent: 'p1' },
  { id: 'e2', type: 'Event', title: 'The city opens its mind', summary: 'Millions donate a single memory to create the Archive.', tone: 'light', parent: 'p2' },
  { id: 'e3', type: 'Event', title: 'The silence referendum', summary: 'Citizens vote on whether the Archive must forget the war.', tone: 'dark', parent: 'p3' },
  { id: 's1', type: 'Scene', title: 'A name at the threshold', summary: 'Who does the Archive recognize as its first visitor?', tone: 'light', parent: 'e2' },
  { id: 's2', type: 'Scene', title: 'The curator refuses', summary: 'Why does the curator deny the emperor access?', tone: 'dark', parent: 'e2' },
]

const initialPlayers = [
  { id: 1, name: 'Quinn', kind: 'Human', prompt: 'Curious, grounded, interested in human consequences.' },
  { id: 2, name: 'Mara', kind: 'AI', prompt: 'A tragic historian. Finds costs hidden inside progress.' },
  { id: 3, name: 'Ivo', kind: 'AI', prompt: 'A bold myth-maker. Introduces strange but coherent reversals.' },
]

const turnSteps = [
  ['Declare focus', 'Name the thread that every contribution must address.'],
  ['Lens creates', 'Create one or two nested pieces of history.'],
  ['Table creates', 'Each other player creates one piece of history.'],
  ['Lens finishes', 'The Lens creates one final piece.'],
  ['Choose legacy', 'The player to the Lens’s right names a Legacy.'],
  ['Explore legacy', 'That player creates an Event or dictated Scene.'],
]

function Icon({ children }) { return <span className="icon">{children}</span> }

function Setup({ players, setPlayers, onStart }) {
  const update = (id, key, value) => setPlayers(players.map(p => p.id === id ? { ...p, [key]: value } : p))
  const addPlayer = () => setPlayers([...players, { id: Date.now(), name: `Player ${players.length + 1}`, kind: 'Human', prompt: '' }])
  return <main className="setup-shell">
    <section className="setup-copy">
      <div className="brand"><span className="brand-mark">M</span> MICROSCOPE <em>AI</em></div>
      <p className="eyebrow">A history engine for humans and agents</p>
      <svg className="history-moon" viewBox="0 0 480 480" role="img" aria-labelledby="history-moon-title">
        <title id="history-moon-title">A thin gold crescent surrounding three histories branching downward</title>
        <defs>
          <mask id="history-moon-crescent" maskUnits="userSpaceOnUse" x="0" y="0" width="480" height="480">
            <rect width="480" height="480" fill="black" />
            <circle cx="240" cy="240" r="204" fill="white" />
            <circle cx="264.086716" cy="240" r="193.086716" fill="black" />
          </mask>
        </defs>
        <circle cx="240" cy="240" r="204" fill="currentColor" mask="url(#history-moon-crescent)" />
        <g fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
          <path d="M160 158V188M140 220V188H180V220 M240 158V188M220 220V188H260V220 M320 158V188M300 220V188H340V220" />
          <path d="M140 240V268H122V305 M180 240V278H193V318 M220 240V263H235V299 M260 240V279H272V327 M300 240V266H312V306 M340 240V275H358V318" />
        </g>
        <g fill="currentColor">
          <circle cx="160" cy="146" r="13" />
          <rect x="228" y="134" width="24" height="24" rx="2" />
          <path d="M320 130L336 146L320 162L304 146Z" />
          <rect x="130" y="220" width="20" height="20" rx="2" />
          <circle cx="180" cy="230" r="10" />
          <path d="M220 217L233 230L220 243L207 230Z" />
          <path d="M260 219L272 240H248Z" />
          <circle cx="300" cy="230" r="10" />
          <rect x="330" y="220" width="20" height="20" rx="2" />
          <circle cx="122" cy="313" r="8" />
          <path d="M193 316L204 335H182Z" />
          <rect x="227" y="299" width="16" height="16" rx="1" />
          <path d="M272 326L283 337L272 348L261 337Z" />
          <path d="M312 304L323 323H301Z" />
          <circle cx="358" cy="326" r="8" />
        </g>
      </svg>
      <p className="lede">Configure your table, then let the game guide each Lens, card, and scene without deciding the history for you.</p>
      <div className="rule-strip"><span>NO GM</span><span>NON-LINEAR</span><span>2–5 PLAYERS</span></div>
    </section>
    <section className="setup-panel">
      <div className="panel-heading"><div><small>NEW HISTORY</small><h2>Who is at the table?</h2></div><span className="count">{players.length}/5</span></div>
      <div className="players">
        {players.map((p, index) => <article className="player-row" key={p.id}>
          <span className="seat">{String(index + 1).padStart(2, '0')}</span>
          <div className="player-fields">
            <input aria-label={`Player ${index + 1} name`} value={p.name} onChange={e => update(p.id, 'name', e.target.value)} />
            <div className="kind-switch">
              {['Human','AI'].map(k => <button className={p.kind === k ? 'active' : ''} onClick={() => update(p.id, 'kind', k)} key={k}>{k}</button>)}
            </div>
            {p.kind === 'AI' && <textarea aria-label={`${p.name} characteristics`} value={p.prompt} onChange={e => update(p.id, 'prompt', e.target.value)} placeholder="Voice, interests, boundaries, creative instincts…" />}
          </div>
          {players.length > 2 && <button className="remove" aria-label={`Remove ${p.name}`} onClick={() => setPlayers(players.filter(x => x.id !== p.id))}>×</button>}
        </article>)}
      </div>
      {players.length < 5 && <button className="add-player" onClick={addPlayer}>+ Add a seat</button>}
      <button className="primary" onClick={onStart}>Begin history <span>→</span></button>
      <p className="privacy">AI seats are profiles only in this prototype. Model and RAG connections come next.</p>
    </section>
  </main>
}

function CardTile({ card, selected, onClick }) {
  return <button className={`card-tile ${card.type.toLowerCase()} ${card.tone} ${selected ? 'selected' : ''}`} onClick={onClick}>
    <span className="card-meta">{card.type} · {card.tone}</span><strong>{card.title}</strong><p>{card.summary}</p>
  </button>
}

function Game({ players, onExit }) {
  const [cards, setCards] = useState(seedCards)
  const [selectedId, setSelectedId] = useState('e2')
  const [step, setStep] = useState(1)
  const [railOpen, setRailOpen] = useState(true)
  const selected = cards.find(c => c.id === selectedId) || cards[0]
  const parent = cards.find(c => c.id === selected.parent)
  const children = cards.filter(c => c.parent === selected.id)
  const periods = cards.filter(c => c.type === 'Period')
  const activePlayer = players[0]
  const breadcrumb = useMemo(() => {
    const out=[]; let current=selected
    while(current){ out.unshift(current); current=cards.find(c=>c.id===current.parent) }
    return out
  }, [selected, cards])

  const addChild = () => {
    const nextType = selected.type === 'History' ? 'Period' : selected.type === 'Period' ? 'Event' : 'Scene'
    if (selected.type === 'Scene') return
    const item={ id:`c${Date.now()}`, type:nextType, title:`Untitled ${nextType}`, summary:'A new piece of history, ready to be described.', tone:'light', parent:selected.id }
    setCards([...cards,item]); setSelectedId(item.id)
  }

  return <main className="game-shell">
    <header className="topbar">
      <button className="logo-button" onClick={onExit}><span className="brand-mark">M</span></button>
      <div className="history-title"><small>HISTORY</small><strong>{cards[0].title}</strong></div>
      <div className="focus-pill"><small>CURRENT FOCUS</small><span>The price of a perfect memory</span></div>
      <div className="avatars">{players.map((p,i)=><span className={i===0?'current':''} title={`${p.name} · ${p.kind}`} key={p.id}>{p.name.slice(0,1)}</span>)}</div>
      <button className="quiet">•••</button>
    </header>

    <aside className={`turn-rail ${railOpen?'':'closed'}`}>
      <button className="rail-toggle" onClick={()=>setRailOpen(!railOpen)}>{railOpen?'‹':'›'}</button>
      <div className="turn-owner"><small>ROUND 01 · LENS</small><div><span>{activePlayer.name.slice(0,1)}</span><strong>{activePlayer.name}</strong></div></div>
      <div className="steps">{turnSteps.map((s,i)=><button key={s[0]} onClick={()=>setStep(i)} className={i===step?'active':i<step?'done':''}><span>{i<step?'✓':i+1}</span><div><strong>{s[0]}</strong><p>{s[1]}</p></div></button>)}</div>
      <div className="prompt-box"><small>YOUR TURN</small><strong>{turnSteps[step][0]}</strong><p>{turnSteps[step][1]}</p><button onClick={()=>setStep(Math.min(step+1,turnSteps.length-1))}>Mark complete →</button></div>
    </aside>

    <section className="workspace">
      <nav className="breadcrumbs">{breadcrumb.map((c,i)=><span key={c.id}>{i>0 && ' / '}<button onClick={()=>setSelectedId(c.id)}>{c.title}</button></span>)}</nav>
      <div className="timeline">
        {periods.map(period => <section className={`period-column ${period.tone}`} key={period.id}>
          <button className="period-head" onClick={()=>setSelectedId(period.id)}><small>{period.type}</small><strong>{period.title}</strong></button>
          <div className="event-stack">{cards.filter(c=>c.parent===period.id).map(event=><CardTile card={event} selected={selectedId===event.id} onClick={()=>setSelectedId(event.id)} key={event.id}/>)}</div>
        </section>)}
      </div>
    </section>

    <aside className="inspector">
      <div className="inspector-top"><span className={`tone-dot ${selected.tone}`}></span><span>{selected.type}</span><button>×</button></div>
      <h2>{selected.title}</h2><p className="summary">{selected.summary}</p>
      <div className="tone-choice"><button className={selected.tone==='light'?'active':''}>☀ Light</button><button className={selected.tone==='dark'?'active':''}>● Dark</button></div>
      {parent && <section className="relation"><small>PARENT</small><button onClick={()=>setSelectedId(parent.id)}><span>{parent.type}</span><strong>{parent.title}</strong><b>↑</b></button></section>}
      <section className="relation"><div className="relation-label"><small>CHILDREN</small><span>{children.length}</span></div>{children.map(c=><button onClick={()=>setSelectedId(c.id)} key={c.id}><span>{c.type}</span><strong>{c.title}</strong><b>→</b></button>)}{selected.type!=='Scene'&&<button className="add-child" onClick={addChild}>+ Add {selected.type==='History'?'Period':selected.type==='Period'?'Event':'Scene'}</button>}</section>
      <section className="notes"><small>THREAD NOTES</small><textarea defaultValue="The Archive recognizes people by what they are willing to forget." /></section>
    </aside>
  </main>
}

export default function App() {
  const [screen, setScreen] = useState("setup");
  const [players, setPlayers] = useState(initialPlayers);

  async function testCreateGame() {
    try {
      const game = await createGame({
        title: "The empire learns to remember",
        bigPicture: "A civilization discovers that memory can be mined.",
        players: [
          {
            name: "Quinn",
            controller: "human",
            personaPrompt: null,
          },
          {
            name: "Mara",
            controller: "ai",
            personaPrompt: "A tragic historian.",
          },
        ],
      });

      console.log("Created game:", game);

      // Navigate only after creation succeeds.
      setScreen("game");
    } catch (error) {
      console.error("Creation failed:", error);
    }
  }

  return screen === "setup" ? (
    <Setup
      players={players}
      setPlayers={setPlayers}
      onStart={testCreateGame}
    />
  ) : (
    <Game
      players={players}
      onExit={() => setScreen("setup")}
    />
  );
}