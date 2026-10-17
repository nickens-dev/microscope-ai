import { useMemo, useState } from 'react'

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
      <h1>Build a history.<br/><i>Discover what it means.</i></h1>
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
  const [screen,setScreen]=useState('setup')
  const [players,setPlayers]=useState(initialPlayers)
  return screen==='setup' ? <Setup players={players} setPlayers={setPlayers} onStart={()=>setScreen('game')} /> : <Game players={players} onExit={()=>setScreen('setup')} />
}
