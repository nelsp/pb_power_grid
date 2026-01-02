import PowerPlantCard from './PowerPlantCard'
import styles from './PlayerPanel.module.css'

const PLAYER_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

const RESOURCE_COLORS = {
  coal: '#8B4513',    // Brown
  oil: '#000000',     // Black
  gas: '#4169E1',     // Blue
  uranium: '#DC143C'  // Red
}

function PlayerPanel({ player, playerIndex }) {
  const borderColor = PLAYER_COLORS[playerIndex % PLAYER_COLORS.length]

  // Calculate resource capacity
  const calculateCapacity = () => {
    const capacity = { coal: 0, oil: 0, gas: 0, uranium: 0 }

    player.cards.forEach(card => {
      const resourceCost = card.resource_cost
      const resourceType = card.resource

      if (['coal', 'oil', 'gas', 'uranium'].includes(resourceType)) {
        capacity[resourceType] += resourceCost * 2
      } else if (resourceType === 'nuclear') {
        capacity.uranium += resourceCost * 2
      } else if (resourceType === 'oil&gas') {
        capacity.oil += resourceCost * 2
        capacity.gas += resourceCost * 2
      }
    })

    return capacity
  }

  const capacity = calculateCapacity()

  return (
    <div className={styles.panel} style={{ borderColor }}>
      <div className={styles.header}>
        <h3 className={styles.playerName} style={{ color: borderColor }}>
          {player.name}
        </h3>
        <div className={styles.money}>${player.money}</div>
      </div>

      <div className={styles.plants}>
        {player.cards.map((card, index) => (
          <PowerPlantCard key={index} card={card} size="small" />
        ))}
      </div>

      <div className={styles.resources}>
        <div className={styles.resourceLabel}>Resources:</div>
        {['coal', 'oil', 'gas', 'uranium'].map(type => {
          const current = player.resources[type] || 0
          const max = capacity[type]
          if (max > 0 || current > 0) {
            return (
              <div key={type} className={styles.resourceRow}>
                <div
                  className={styles.resourceCircle}
                  style={{ backgroundColor: RESOURCE_COLORS[type] }}
                  title={type}
                />
                <span className={styles.resourceAmount}>
                  {current}/{max}
                </span>
              </div>
            )
          }
          return null
        })}
      </div>
    </div>
  )
}

export default PlayerPanel
