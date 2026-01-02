# Power Grid Game State Visualizer

A lightweight React web application for visualizing Power Grid game replay files.

## Features

- 📁 Drag & drop JSON file upload
- 🎮 Interactive game state navigation (previous/next)
- 🗺️ City network graph visualization with player occupancy
- 🏭 Power plant market display (current and future)
- 👥 Player panels showing cards, resources, and money
- 📱 Responsive design with dynamic resizing

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **vis-network** - Graph visualization
- **CSS Modules** - Scoped styling

**Total bundle size**: ~134 KB (gzipped)

## Quick Start

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
# Navigate to the visualizer directory
cd power-grid-visualizer

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open at `http://localhost:5173`

### Build for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

The production files will be in the `dist/` folder.

## Usage

1. **Upload a game file**:
   - Drag and drop a `power_grid_game_log.json` file onto the upload area
   - Or click "Browse Files" to select a file

2. **Navigate game states**:
   - Use Previous/Next buttons to step through the game
   - Current step and game phase are shown in the header

3. **View game state**:
   - **Top section**: Power plant markets (current and future)
   - **Middle section**: City network graph (colored by player occupation)
   - **Bottom section**: Player panels with cards, resources, and money

## Project Structure

```
power-grid-visualizer/
├── src/
│   ├── components/
│   │   ├── CityGraph.jsx         # Network graph visualization
│   │   ├── FileUpload.jsx        # Drag & drop file upload
│   │   ├── GameStateViewer.jsx   # Main game state layout
│   │   ├── MarketPanel.jsx       # Power plant markets
│   │   ├── PlayerPanel.jsx       # Individual player display
│   │   └── PowerPlantCard.jsx    # Card component
│   ├── App.jsx                   # Main app component
│   ├── main.jsx                  # React entry point
│   └── index.css                 # Global styles
├── public/
│   └── assets/
│       └── cards/
│           └── images/           # Power plant card images
├── index.html
├── vite.config.js
└── package.json
```

## Card Images

Card images should be placed in `public/assets/cards/images/` with the naming format:
- `03.png` for power plant cost 3
- `04.png` for power plant cost 4
- etc.

If a card image is missing, a text fallback will be displayed.

## Development

### Dev Server

```bash
npm run dev
```

Features:
- Hot module replacement (HMR)
- Fast refresh for React components
- Instant updates on file changes

### Adding Features

The codebase uses:
- **CSS Modules** for component styling (`.module.css` files)
- **React hooks** for state management
- **vis-network** for graph rendering

No additional libraries are needed for basic features.

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

Requires modern browser with ES2020 support.

## License

MIT
