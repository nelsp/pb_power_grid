import styles from './AuctionOverlay.module.css'

function AuctionOverlay({ gameState }) {
  const {
    auction_active,
    auction_plant,
    auction_current_bid,
    auction_current_winner,
    auction_active_bidders,
    auction_starter,
    players
  } = gameState

  // Don't render if auction is not active
  if (!auction_active || !auction_plant) {
    return null
  }

  // Get plant image URL (same as MarketPanel)
  const getPlantImageUrl = (plant) => {
    return `/power-plants/${plant.cost}.jpg`
  }

  return (
    <div className={styles.auctionPanel}>
      <div className={styles.header}>
        <h2>🔨 Auction in Progress</h2>
      </div>

      <div className={styles.content}>
        {/* Plant Card with Image */}
        <div className={styles.plantCard}>
          <img
            src={getPlantImageUrl(auction_plant)}
            alt={`Power Plant ${auction_plant.cost}`}
            className={styles.plantImage}
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
          <div className={styles.plantInfo}>
            <div className={styles.plantCost}>{auction_plant.cost}€</div>
            <div className={styles.plantPower}>
              Powers {auction_plant.cities} {auction_plant.cities === 1 ? 'city' : 'cities'}
            </div>
          </div>
        </div>

        {/* Current Bid Info */}
        <div className={styles.currentBid}>
          <div className={styles.bidLabel}>Current Bid</div>
          <div className={styles.bidAmount}>{auction_current_bid}€</div>
          <div className={styles.bidder}>
            by {players[auction_current_winner]?.name || `Player ${auction_current_winner}`}
          </div>
        </div>

        {/* Active Bidders */}
        <div className={styles.bidders}>
          <h3>Bidders</h3>
          <div className={styles.biddersList}>
              {/* Starter (current winner if they opened) */}
              <div
                className={`${styles.bidderCard} ${
                  auction_current_winner === auction_starter ? styles.winning : styles.passed
                }`}
              >
                <div className={styles.bidderName}>
                  {players[auction_starter]?.name || `Player ${auction_starter}`}
                  <span className={styles.badge}>Opener</span>
                </div>
                <div className={styles.bidderStatus}>
                  {auction_current_winner === auction_starter ? (
                    <span className={styles.winningBadge}>✓ Winning at {auction_current_bid}€</span>
                  ) : (
                    <span className={styles.passedBadge}>Passed</span>
                  )}
                </div>
              </div>

              {/* Active bidders */}
              {auction_active_bidders.map(playerIdx => (
                <div
                  key={playerIdx}
                  className={`${styles.bidderCard} ${
                    auction_current_winner === playerIdx ? styles.winning : styles.active
                  }`}
                >
                  <div className={styles.bidderName}>
                    {players[playerIdx]?.name || `Player ${playerIdx}`}
                  </div>
                  <div className={styles.bidderStatus}>
                    {auction_current_winner === playerIdx ? (
                      <span className={styles.winningBadge}>✓ Winning at {auction_current_bid}€</span>
                    ) : (
                      <span className={styles.activeBadge}>Active</span>
                    )}
                  </div>
                  <div className={styles.bidderMoney}>
                    {players[playerIdx]?.money}€ available
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AuctionOverlay
