import styles from './PowerPlantCard.module.css'

function PowerPlantCard({ card, size = 'normal' }) {
  const cardImagePath = `/assets/cards/images/${String(card.cost).padStart(2, '0')}.png`

  return (
    <div className={`${styles.card} ${styles[size]}`}>
      <img
        src={cardImagePath}
        alt={`Power plant ${card.cost}`}
        className={styles.cardImage}
        onError={(e) => {
          // Fallback to text rendering if image doesn't load
          e.target.style.display = 'none'
          e.target.nextSibling.style.display = 'flex'
        }}
      />
      <div className={styles.fallback}>
        <div className={styles.cost}>{card.cost}</div>
        <div className={styles.resource}>{card.resource}</div>
        <div className={styles.cities}>⚡ {card.cities}</div>
      </div>
    </div>
  )
}

export default PowerPlantCard
