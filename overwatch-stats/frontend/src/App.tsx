import './App.css'
import Search from './components/Search'

function App() {
  return (
    <main className="app-shell">
      <header className="page-header">
        <p className="intro">
          Search a BattleTag to pull up a player profile from Overfast.
        </p>
      </header>
      <Search />
    </main>
  )
}

export default App
