import PowerPlantCard from './PowerPlantCard'
import styles from './MarketPanel.module.css'

function MarketPanel({ currentMarket, futureMarket }) {
  return (
    <div className={styles.container}>
      <div className={styles.marketRow}>
        <div className={styles.label}>Current Market</div>
        <div className={styles.cards}>
          {currentMarket && currentMarket.map((card, index) => (
            <PowerPlantCard key={index} card={card} />
          ))}
        </div>
      </div>

      {futureMarket && futureMarket.length > 0 && (
        <div className={styles.marketRow}>
          <div className={styles.label}>Future Market</div>
          <div className={styles.cards}>
            {futureMarket.map((card, index) => (
              <PowerPlantCard key={index} card={card} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default MarketPanel
