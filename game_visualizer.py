import json
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
import networkx as nx
from matplotlib.widgets import Button
from board_setup import pos, europe


class GameVisualizer:
    def __init__(self, json_file=None):
        self.game_data = None
        self.current_step = 0
        self.fig = None
        self.axes = {}
        self.card_image_cache = {}

        if json_file:
            self.load_game_file(json_file)

    def load_game_file(self, filename):
        try:
            with open(filename, 'r') as f:
                self.game_data = json.load(f)
            print(f"Loaded game with {len(self.game_data)} steps")
        except Exception as e:
            print(f"Error loading file: {e}")

    def visualize_step(self, step_number=0):
        if not self.game_data:
            self.show_upload_message()
            return

        self.current_step = step_number
        if self.current_step >= len(self.game_data):
            self.current_step = 0
        if self.current_step < 0:
            self.current_step = len(self.game_data) - 1

        game_state = self.game_data[self.current_step]['gameState']

        # Create figure with dark background (only first time)
        if self.fig is None:
            self.fig = plt.figure(figsize=(20, 12), facecolor='#2b2b2b')

            # Create grid layout with space for buttons
            gs = self.fig.add_gridspec(4, 1, height_ratios=[1, 2.5, 1.2, 0.15], hspace=0.3)

            # Market board (top)
            self.axes['market'] = self.fig.add_subplot(gs[0])
            self.axes['market'].set_facecolor('#2b2b2b')

            # Map (middle - larger)
            self.axes['map'] = self.fig.add_subplot(gs[1])
            self.axes['map'].set_facecolor('#2b2b2b')

            # Player areas
            self.axes['players'] = self.fig.add_subplot(gs[2])
            self.axes['players'].set_facecolor('#2b2b2b')

            # Navigation buttons
            ax_prev = plt.axes([0.3, 0.02, 0.15, 0.04])
            ax_next = plt.axes([0.55, 0.02, 0.15, 0.04])

            self.btn_prev = Button(ax_prev, 'Previous', color='#555555', hovercolor='#777777')
            self.btn_next = Button(ax_next, 'Next', color='#555555', hovercolor='#777777')

            self.btn_prev.on_clicked(lambda event: self.prev_step())
            self.btn_next.on_clicked(lambda event: self.next_step())

        # Clear and render all components
        for ax in self.axes.values():
            ax.clear()
            ax.set_facecolor('#2b2b2b')

        self.render_market(self.axes['market'], game_state['current_market'], game_state['future_market'])
        self.render_map(self.axes['map'], game_state)
        self.render_players(self.axes['players'], game_state['players'])

        # Get game phase and format it nicely
        phase = game_state.get('phase', 'unknown')
        phase_display = phase.replace('_', ' ').title()

        # Get game step
        game_step = game_state.get('step', 1)

        self.fig.suptitle(f"Power Grid Game - Step {self.current_step} of {len(self.game_data)-1} (Game Step {game_step} - {phase_display})",
                         color='white', fontsize=16, y=0.98)

        # Force a complete redraw
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def next_step(self):
        if self.game_data and self.current_step < len(self.game_data) - 1:
            self.visualize_step(self.current_step + 1)

    def prev_step(self):
        if self.game_data and self.current_step > 0:
            self.visualize_step(self.current_step - 1)

    def show_upload_message(self):
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#3c3c3c')
        ax.set_facecolor('#3c3c3c')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        ax.text(5, 5, 'Upload a game replay',
               ha='center', va='center', fontsize=32,
               color='#888888', weight='bold')
        ax.text(5, 3.5, 'Run: python3 game_visualizer.py <path_to_json>',
               ha='center', va='center', fontsize=14,
               color='#666666')

        plt.show()

    def load_card_image(self, card_number):
        """Load and cache card image"""
        if card_number in self.card_image_cache:
            return self.card_image_cache[card_number]

        # Format card number with leading zero (e.g., 03, 04, etc.)
        card_file = f"{card_number:02d}.png"
        card_path = os.path.join('assets', 'cards', 'images', card_file)

        try:
            if os.path.exists(card_path):
                img = mpimg.imread(card_path)
                self.card_image_cache[card_number] = img
                return img
        except Exception as e:
            print(f"Error loading card image {card_path}: {e}")

        return None

    def render_market(self, ax, current_market, future_market):
        ax.axis('off')

        # Card dimensions - larger square size
        card_size = 22
        padding = 4

        # Calculate total width needed based on max cards in either row
        num_current = len(current_market)
        num_future = len(future_market)
        max_cards = max(num_current, num_future, 4)  # At least space for 4 cards

        # Set coordinate system to accommodate all cards with margins
        margin = 5
        total_width = max_cards * card_size + (max_cards - 1) * padding + 2 * margin
        total_height = 100
        ax.set_xlim(0, total_width)
        ax.set_ylim(0, total_height)

        # Current market: top row (centered)
        if num_current > 0:
            current_total_width = num_current * card_size + (num_current - 1) * padding
            current_start_x = (total_width - current_total_width) / 2
            current_y = 70  # Top row

            # Draw current market cards in a single row
            for i, card in enumerate(current_market):
                x = current_start_x + i * (card_size + padding)
                self.draw_power_plant_card(ax, card, x, current_y, card_size, card_size)

        # Future market: bottom row (centered)
        if num_future > 0:
            future_total_width = num_future * card_size + (num_future - 1) * padding
            future_start_x = (total_width - future_total_width) / 2
            future_y = 30  # Bottom row

            # Draw future market cards in a single row
            for i, card in enumerate(future_market):
                x = future_start_x + i * (card_size + padding)
                self.draw_power_plant_card(ax, card, x, future_y, card_size, card_size)

    def draw_power_plant_card(self, ax, card, x, y, width, height):
        """Draw a power plant card using the actual card image as a square"""
        card_number = card['cost']

        # Try to load the card image
        img = self.load_card_image(card_number)

        if img is not None:
            # Display the actual card image - force square aspect ratio
            extent = [x, x + width, y - height, y]  # y goes down from starting point
            ax.imshow(img, extent=extent, aspect='equal', zorder=2, interpolation='bilinear')
        else:
            # Fallback: draw text-based card if image not found
            rect = mpatches.Rectangle((x, y - height), width, height,
                                     facecolor='#1a1a1a', edgecolor='#666666', linewidth=2)
            ax.add_patch(rect)

            # Card cost
            ax.text(x + width/2, y - height*0.3, str(card['cost']),
                   ha='center', va='center', fontsize=12,
                   color='#FFD700', weight='bold')

            # Resource type
            resource_colors = {
                'coal': '#4a4a4a',
                'oil': '#8B4513',
                'gas': '#FFA500',
                'uranium': '#00FF00',
                'green': '#90EE90',
                'oil&gas': '#CD853F'
            }
            color = resource_colors.get(card['resource'], '#888888')
            ax.text(x + width/2, y - height/2, card['resource'][:3].upper(),
                   ha='center', va='center', fontsize=8,
                   color=color)

            # Cities powered
            ax.text(x + width/2, y - height*0.7, f"⚡{card['cities']}",
                   ha='center', va='center', fontsize=8,
                   color='white')

    def render_map(self, ax, game_state):
        # Create networkx graph
        G = nx.Graph()

        # Get all European cities from board_setup - ensure consistent ordering
        all_cities = sorted(list(pos.keys()))  # Sort for consistent ordering
        G.add_nodes_from(all_cities)

        # Add edges from europe data
        for edge in europe:
            city1 = edge[0][1]
            city2 = edge[1][1]
            cost = edge[2]
            if city1 in pos and city2 in pos:
                G.add_edge(city1, city2, weight=cost)

        # Color nodes based on occupation
        node_colors = []
        player_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

        occupied_cities = {}
        for i, player in enumerate(game_state['players']):
            for city in player['generators']:
                if city not in occupied_cities:
                    occupied_cities[city] = []
                occupied_cities[city].append(i)

        for city in all_cities:
            if city in occupied_cities:
                # Use first player's color who occupies this city
                node_colors.append(player_colors[occupied_cities[city][0]])
            else:
                node_colors.append('#3c3c3c')

        # Set axis limits to fixed values to prevent graph from moving/scaling
        # Get bounds from position data
        if pos:
            x_coords = [coord[0] for coord in pos.values()]
            y_coords = [coord[1] for coord in pos.values()]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            # Add padding (10%)
            x_padding = (x_max - x_min) * 0.1
            y_padding = (y_max - y_min) * 0.1

            ax.set_xlim(x_min - x_padding, x_max + x_padding)
            ax.set_ylim(y_min - y_padding, y_max + y_padding)

        # Draw the network with fixed positions
        nx.draw_networkx_edges(G, pos, alpha=0.3, width=1,
                             edge_color='#666666', ax=ax)

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                             node_size=300, ax=ax,
                             edgecolors='#888888', linewidths=1)

        # Draw labels with better visibility
        nx.draw_networkx_labels(G, pos, font_size=7,
                              font_color='white', font_weight='bold', ax=ax)

        ax.axis('off')
        ax.set_aspect('equal')  # Ensure equal aspect ratio
        ax.set_title('Europe Map', color='white', fontsize=12, pad=10)

    def calculate_resource_capacity(self, player):
        """Calculate total resource capacity for a player based on their power plants"""
        capacity = {'coal': 0, 'oil': 0, 'gas': 0, 'uranium': 0}

        for card in player['cards']:
            resource_type = card['resource']
            resource_cost = card['resource_cost']

            if resource_type in ['coal', 'oil', 'gas', 'uranium']:
                # Each plant can store 2x its consumption
                capacity[resource_type] += resource_cost * 2
            elif resource_type == 'nuclear':
                capacity['uranium'] += resource_cost * 2
            elif resource_type == 'oil&gas':
                # Hybrid plants: total capacity split between oil and gas
                total_cap = resource_cost * 2
                capacity['oil'] += total_cap
                capacity['gas'] += total_cap

        return capacity

    def render_players(self, ax, players):
        # Dynamic coordinate system
        total_width = 100
        total_height = 100
        ax.set_xlim(0, total_width)
        ax.set_ylim(0, total_height)
        ax.axis('off')

        player_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

        num_players = len(players)
        box_width = (total_width - 5) / num_players - 2
        box_height = 80

        for i, player in enumerate(players):
            x = 2.5 + i * (box_width + 2)

            # Player box
            rect = mpatches.Rectangle((x, 10), box_width, box_height,
                                     facecolor='#1a1a1a',
                                     edgecolor=player_colors[i],
                                     linewidth=3)
            ax.add_patch(rect)

            # Player name
            ax.text(x + box_width/2, 88, player['name'],
                   ha='center', va='top', fontsize=9,
                   color=player_colors[i], weight='bold')

            # Money
            ax.text(x + box_width/2, 79, f"${player['money']}",
                   ha='center', va='top', fontsize=12,
                   color='#FFD700', weight='bold')

            # Power plants - draw actual card images
            cards = player['cards']
            if cards:
                card_size = min(8, box_width / len(cards) - 1)  # Dynamic sizing
                total_cards_width = len(cards) * card_size + (len(cards) - 1) * 0.5
                cards_start_x = x + (box_width - total_cards_width) / 2
                cards_y = 58

                for j, card in enumerate(cards):
                    card_x = cards_start_x + j * (card_size + 0.5)
                    self.draw_power_plant_card(ax, card, card_x, cards_y, card_size, card_size)

            # Resources with capacity
            resources = player['resources']
            capacity = self.calculate_resource_capacity(player)

            resource_y = 35
            ax.text(x + box_width/2, resource_y, 'Resources:',
                   ha='center', va='top', fontsize=7,
                   color='white')

            # Display each resource type
            resource_colors_display = {
                'coal': '#888888',
                'oil': '#CD853F',
                'gas': '#FFA500',
                'uranium': '#00FF00'
            }

            resource_labels = {
                'coal': 'Coal',
                'oil': 'Oil',
                'gas': 'Gas',
                'uranium': 'Ura'
            }

            y_offset = resource_y - 5
            for res_type in ['coal', 'oil', 'gas', 'uranium']:
                current = resources.get(res_type, 0)
                cap = capacity.get(res_type, 0)
                color = resource_colors_display[res_type]

                if cap > 0 or current > 0:  # Only show if player has capacity or resources
                    text = f"{resource_labels[res_type]}: {current}/{cap}"
                    ax.text(x + box_width/2, y_offset, text,
                           ha='center', va='top', fontsize=6,
                           color=color)
                    y_offset -= 4


def main():
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        viz = GameVisualizer(json_file)
        viz.visualize_step(0)
        plt.show()  # Keep window open
    else:
        viz = GameVisualizer()
        viz.show_upload_message()


if __name__ == '__main__':
    main()
