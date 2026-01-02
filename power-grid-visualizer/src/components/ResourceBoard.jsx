import styles from './ResourceBoard.module.css'

const RESOURCE_COLORS = {
  coal: '#8B4513',    // Brown
  oil: '#000000',     // Black
  gas: '#4169E1',     // Blue
  uranium: '#DC143C'  // Red
}

function ResourceBoard({ resources }) {
  const renderResourceTrack = (resourceType) => {
    if (!resources || !resources[resourceType]) {
      return null
    }

    const resource = resources[resourceType]
    const capacityList = resource.capacity_list || []

    return (
      <div key={resourceType} className={styles.resourceTrack}>
        <div className={styles.resourceHeader}>
          <div
            className={styles.resourceDot}
            style={{ backgroundColor: RESOURCE_COLORS[resourceType] }}
          />
          <span className={styles.resourceName}>{resourceType}</span>
        </div>

        <div className={styles.priceTrack}>
          {capacityList.map(([price, slots], tierIndex) => {
            return (
              <div key={tierIndex} className={styles.priceTier}>
                <div className={styles.priceLabel}>{price}</div>
                <div className={styles.slots}>
                  {slots.map((filled, slotIndex) => (
                    <div
                      key={slotIndex}
                      className={styles.slot}
                      style={{
                        backgroundColor: filled === 1
                          ? RESOURCE_COLORS[resourceType]
                          : '#444',
                        border: `1px solid ${filled === 1 ? '#fff' : '#666'}`
                      }}
                    />
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  return (
    <div className={styles.board}>
      <h3 className={styles.boardTitle}>Resource Market</h3>
      <div className={styles.tracks}>
        {renderResourceTrack('coal')}
        {renderResourceTrack('oil')}
        {renderResourceTrack('gas')}
        {renderResourceTrack('uranium')}
      </div>
    </div>
  )
}

export default ResourceBoard
