import { useEffect, useRef } from 'react'
import { Network } from 'vis-network/standalone'
import styles from './CityGraph.module.css'

const PLAYER_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
const SLOT_COSTS = [10, 15, 20]

function CityGraph({ boardGraph, cityOccupancy, players, step }) {
  const containerRef = useRef(null)
  const networkRef = useRef(null)
  const nodePositionsRef = useRef(null)
  const initializedRef = useRef(false)
  const overlayContainerRef = useRef(null)
  const viewportRef = useRef(null)

  // Create DOM element for a city node overlay
  const createCityNodeElement = (cityName, occupants, currentStep) => {
    const div = document.createElement('div')
    div.className = styles.cityNode
    div.style.position = 'absolute'
    div.style.transform = 'translate(-50%, -50%)'
    div.style.pointerEvents = 'none'
    div.style.background = 'rgba(0, 0, 0, 0.85)'
    div.style.padding = '6px 8px'
    div.style.borderRadius = '6px'
    div.style.border = '2px solid #555'
    div.style.minWidth = '70px'
    div.style.boxShadow = '0 2px 8px rgba(0,0,0,0.5)'

    // City name
    const nameDiv = document.createElement('div')
    nameDiv.textContent = cityName
    nameDiv.style.fontWeight = 'bold'
    nameDiv.style.fontSize = '11px'
    nameDiv.style.color = '#fff'
    nameDiv.style.textAlign = 'center'
    nameDiv.style.marginBottom = '4px'
    div.appendChild(nameDiv)

    // Slots container
    const slotsDiv = document.createElement('div')
    slotsDiv.style.display = 'flex'
    slotsDiv.style.gap = '4px'
    slotsDiv.style.justifyContent = 'center'

    const maxSlots = currentStep || 1

    for (let i = 0; i < 3; i++) {
      const cost = SLOT_COSTS[i]
      const isAvailable = i < maxSlots
      const occupant = occupants && occupants[i] !== undefined ? occupants[i] : null

      const slot = document.createElement('div')
      slot.style.width = '20px'
      slot.style.height = '20px'
      slot.style.borderRadius = '3px'
      slot.style.display = 'flex'
      slot.style.alignItems = 'center'
      slot.style.justifyContent = 'center'
      slot.style.fontSize = '10px'
      slot.style.fontWeight = 'bold'
      slot.style.border = '1px solid rgba(255, 255, 255, 0.3)'

      if (occupant !== null) {
        // Slot is occupied
        const playerColor = PLAYER_COLORS[occupant % PLAYER_COLORS.length]
        slot.style.background = playerColor
        slot.style.color = '#fff'
        slot.textContent = `P${occupant}`
      } else if (isAvailable) {
        // Slot is available but empty
        slot.style.background = '#555'
        slot.style.color = '#aaa'
        slot.textContent = cost.toString()
      } else {
        // Slot is not yet available
        slot.style.background = '#333'
        slot.style.color = '#666'
        slot.style.opacity = '0.5'
        slot.textContent = cost.toString()
      }

      slotsDiv.appendChild(slot)
    }

    div.appendChild(slotsDiv)
    return div
  }

  // Update overlay positions based on network positions
  const updateOverlays = () => {
    if (!networkRef.current || !overlayContainerRef.current) return

    const positions = networkRef.current.getPositions()
    const cityElements = overlayContainerRef.current.children

    Array.from(cityElements).forEach((element) => {
      const cityName = element.dataset.cityName
      if (positions[cityName]) {
        const canvasPos = networkRef.current.canvasToDOM(positions[cityName])
        element.style.left = `${canvasPos.x}px`
        element.style.top = `${canvasPos.y}px`
      }
    })
  }

  useEffect(() => {
    if (!boardGraph || !containerRef.current) return

    const nodes = []
    const edges = []
    const processedEdges = new Set()

    // Parse board graph
    Object.entries(boardGraph).forEach(([cityKey, connections]) => {
      // Parse the city key - it's a string representation of a tuple
      const cityName = cityKey.split(',')[1]?.replace(/[')"\s]/g, '') || cityKey

      if (!nodes.find(n => n.id === cityName)) {
        const nodeData = {
          id: cityName,
          label: '', // No label - we'll use DOM overlay
          color: { background: 'rgba(0,0,0,0)', border: 'rgba(0,0,0,0)' }, // Invisible node
          size: 5, // Small invisible point
          font: { size: 0 },
        }

        // If we have stored positions, use them
        if (nodePositionsRef.current && nodePositionsRef.current[cityName]) {
          nodeData.x = nodePositionsRef.current[cityName].x
          nodeData.y = nodePositionsRef.current[cityName].y
          nodeData.fixed = { x: true, y: true }
        }

        nodes.push(nodeData)
      }

      // Add edges
      Object.entries(connections).forEach(([connectedKey, cost]) => {
        const connectedCity = connectedKey.split(',')[1]?.replace(/[')"\s]/g, '') || connectedKey

        const edgeId = [cityName, connectedCity].sort().join('-')
        if (!processedEdges.has(edgeId)) {
          edges.push({
            from: cityName,
            to: connectedCity,
            label: String(cost),
            font: { color: '#888', size: 8 },
            color: { color: '#444' },
          })
          processedEdges.add(edgeId)
        }
      })
    })

    const data = { nodes, edges }

    const options = {
      nodes: {
        shape: 'dot',
        size: 5,
      },
      edges: {
        width: 2,
        color: { color: '#555' },
        smooth: {
          type: 'continuous',
        },
      },
      physics: {
        enabled: !initializedRef.current, // Enable physics only on first render
        stabilization: {
          enabled: !initializedRef.current,
          iterations: 200,
        },
      },
      interaction: {
        hover: true,
        zoomView: true,
        dragView: true,
      },
      layout: {
        randomSeed: 42, // Fixed seed for consistent layout
      },
    }

    // If network already exists, just update the data
    if (networkRef.current && initializedRef.current) {
      // Save current viewport position and scale
      viewportRef.current = networkRef.current.getViewPosition()
      const currentScale = networkRef.current.getScale()

      networkRef.current.setData(data)

      // Restore viewport after data update
      setTimeout(() => {
        if (viewportRef.current && networkRef.current) {
          networkRef.current.moveTo({
            position: viewportRef.current,
            scale: currentScale,
            animation: false
          })
        }
      }, 0)

      // Update overlays
      setTimeout(() => {
        if (overlayContainerRef.current) {
          overlayContainerRef.current.innerHTML = ''
          Object.entries(boardGraph).forEach(([cityKey]) => {
            const cityName = cityKey.split(',')[1]?.replace(/[')"\s]/g, '') || cityKey
            const occupants = cityOccupancy && cityOccupancy[cityName] ? cityOccupancy[cityName] : []
            const element = createCityNodeElement(cityName, occupants, step)
            element.dataset.cityName = cityName
            overlayContainerRef.current.appendChild(element)
          })
          updateOverlays()
        }
      }, 50)
    } else {
      // Create new network on first render
      if (networkRef.current) {
        networkRef.current.destroy()
      }

      networkRef.current = new Network(containerRef.current, data, options)

      // Store positions after initial stabilization
      if (!initializedRef.current) {
        networkRef.current.once('stabilizationIterationsDone', () => {
          const positions = networkRef.current.getPositions()
          nodePositionsRef.current = positions
          initializedRef.current = true

          // Disable physics after initial layout
          networkRef.current.setOptions({ physics: { enabled: false } })

          // Create overlays after stabilization
          if (overlayContainerRef.current) {
            overlayContainerRef.current.innerHTML = ''
            Object.entries(boardGraph).forEach(([cityKey]) => {
              const cityName = cityKey.split(',')[1]?.replace(/[')"\s]/g, '') || cityKey
              const occupants = cityOccupancy && cityOccupancy[cityName] ? cityOccupancy[cityName] : []
              const element = createCityNodeElement(cityName, occupants, step)
              element.dataset.cityName = cityName
              overlayContainerRef.current.appendChild(element)
            })
            updateOverlays()
          }
        })
      }

      // Update overlays on zoom/pan
      networkRef.current.on('zoom', updateOverlays)
      networkRef.current.on('dragEnd', updateOverlays)
    }

    return () => {
      if (networkRef.current && !initializedRef.current) {
        networkRef.current.destroy()
        networkRef.current = null
      }
    }
  }, [boardGraph, cityOccupancy, step])

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div ref={containerRef} className={styles.graphContainer} />
      <div
        ref={overlayContainerRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none'
        }}
      />
    </div>
  )
}

export default CityGraph
