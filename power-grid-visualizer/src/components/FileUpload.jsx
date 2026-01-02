import { useState } from 'react'
import styles from './FileUpload.module.css'

function FileUpload({ onGameStateLoaded }) {
  const [isDragging, setIsDragging] = useState(false)

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file && file.type === 'application/json') {
      readFile(file)
    }
  }

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    if (file) {
      readFile(file)
    }
  }

  const readFile = (file) => {
    const reader = new FileReader()
    reader.onload = (event) => {
      try {
        const gameStates = JSON.parse(event.target.result)
        onGameStateLoaded(gameStates)
      } catch (error) {
        alert('Error parsing JSON file: ' + error.message)
      }
    }
    reader.readAsText(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  return (
    <div className={styles.container}>
      <div
        className={`${styles.dropzone} ${isDragging ? styles.dragging : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <h2>Upload a game replay</h2>
        <p>Drag and drop a JSON file here</p>
        <p className={styles.or}>or</p>
        <label className={styles.fileButton}>
          <input
            type="file"
            accept=".json,application/json"
            onChange={handleFileInput}
            className={styles.fileInput}
          />
          Browse Files
        </label>
      </div>
    </div>
  )
}

export default FileUpload
