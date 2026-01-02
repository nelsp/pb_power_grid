import { useState } from 'react'
import FileUpload from './components/FileUpload'
import GameStateViewer from './components/GameStateViewer'
import styles from './App.module.css'

function App() {
  const [gameStates, setGameStates] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)

  const currentState = gameStates[currentIndex]

  const handlePrevious = () => {
    setCurrentIndex(i => Math.max(0, i - 1))
  }

  const handleNext = () => {
    setCurrentIndex(i => Math.min(gameStates.length - 1, i + 1))
  }

  const handleNextPhase = () => {
    const currentPhase = gameStates[currentIndex]?.gameState.phase
    for (let i = currentIndex + 1; i < gameStates.length; i++) {
      if (gameStates[i].gameState.phase !== currentPhase) {
        setCurrentIndex(i)
        break
      }
    }
  }

  const handleNextRound = () => {
    const currentRound = gameStates[currentIndex]?.gameState.round_num
    if (currentRound === undefined) return

    for (let i = currentIndex + 1; i < gameStates.length; i++) {
      if (gameStates[i].gameState.round_num > currentRound) {
        setCurrentIndex(i)
        break
      }
    }
  }

  const handleSkip10 = () => {
    setCurrentIndex(i => Math.min(gameStates.length - 1, i + 10))
  }

  return (
    <div className={styles.app}>
      {!currentState ? (
        <FileUpload onGameStateLoaded={setGameStates} />
      ) : (
        <>
          <div className={styles.header}>
            <h1>Power Grid Game Viewer</h1>
            <div className={styles.controls}>
              <button
                onClick={handlePrevious}
                disabled={currentIndex === 0}
                className={styles.button}
              >
                ← Previous
              </button>
              <button
                onClick={handleNext}
                disabled={currentIndex === gameStates.length - 1}
                className={styles.button}
              >
                Next →
              </button>
              <button
                onClick={handleSkip10}
                disabled={currentIndex >= gameStates.length - 10}
                className={styles.button}
              >
                Skip +10
              </button>
              <button
                onClick={handleNextPhase}
                className={styles.button}
              >
                Next Phase
              </button>
              <button
                onClick={handleNextRound}
                className={styles.button}
              >
                Next Round
              </button>
              <span className={styles.stepInfo}>
                Step {currentIndex} of {gameStates.length - 1}
                {currentState.gameState.step && ` (Game Step ${currentState.gameState.step} - ${currentState.gameState.phase})`}
              </span>
            </div>
          </div>
          <GameStateViewer state={currentState.gameState} />
        </>
      )}
    </div>
  )
}

export default App
