import MarketPanel from './MarketPanel'
import PlayerPanel from './PlayerPanel'
import CityGraph from './CityGraph'
import ResourceBoard from './ResourceBoard'
import AuctionOverlay from './AuctionOverlay'
import styles from './GameStateViewer.module.css'

function GameStateViewer({ state }) {
  return (
    <div className={styles.container}>
      {/* Auction Overlay - appears over everything when auction is active */}
      <AuctionOverlay gameState={state} />
      <div className={styles.resourceSection}>
        <ResourceBoard resources={state.resources} />
      </div>

      <div className={styles.mainContent}>
        <div className={styles.marketSection}>
          <MarketPanel
            currentMarket={state.current_market}
            futureMarket={state.future_market}
          />
        </div>

        <div className={styles.mapSection}>
          <CityGraph
            boardGraph={state.board_graph}
            cityOccupancy={state.city_occupancy}
            players={state.players}
            step={state.step}
          />
        </div>

        <div className={styles.playersSection}>
          {state.players.map((player, index) => (
            <PlayerPanel key={index} player={player} playerIndex={index} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default GameStateViewer
