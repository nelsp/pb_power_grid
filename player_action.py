"""
Player Action class for Power Grid
Unified action representation for all player decisions
"""

from enum import Enum
from typing import Optional, Dict, List, Union


class ActionType(Enum):
    """Enumeration of all possible player action types"""
    # Phase 2: Auction
    AUCTION_PASS = 'auction_pass'
    AUCTION_OPEN = 'auction_open'
    AUCTION_BID = 'auction_bid'
    AUCTION_BID_PASS = 'auction_bid_pass'

    # Phase 3: Resources
    RESOURCE_PURCHASE = 'resource_purchase'

    # Phase 4: Building
    CITY_BUILD = 'city_build'

    # Phase 5: Bureaucracy
    POWER_CITIES = 'power_cities'


class PlayerAction:
    """Unified representation of all player actions in Power Grid

    This class encapsulates all possible player decisions with a single interface.
    The action_type determines which fields are relevant.
    """

    def __init__(self, action_type: ActionType,
                 plant=None,
                 bid=None,
                 discard=None,
                 resources=None,
                 cities=None,
                 power_plan=None):
        """
        Args:
            action_type: ActionType enum indicating what kind of action this is
            plant: Card object (for AUCTION_OPEN)
            bid: int bid amount (for AUCTION_OPEN, AUCTION_BID)
            discard: Card object to discard (for AUCTION_OPEN/BID when player has 3 plants)
            resources: dict of {resource_type: amount} (for RESOURCE_PURCHASE)
            cities: list of city names (for CITY_BUILD)
            power_plan: int or list of power plans (for POWER_CITIES)
        """
        self.action_type = action_type
        self.plant = plant
        self.bid = bid
        self.discard = discard
        self.resources = resources if resources is not None else {}
        self.cities = cities if cities is not None else []
        self.power_plan = power_plan

    # Convenience factory methods for creating actions

    @staticmethod
    def auction_pass():
        """Create an action to pass on opening an auction"""
        return PlayerAction(ActionType.AUCTION_PASS)

    @staticmethod
    def auction_open(plant, bid, discard=None):
        """Create an action to open an auction on a plant

        Args:
            plant: Card to auction
            bid: Opening bid amount
            discard: Card to discard if player has 3 plants
        """
        return PlayerAction(ActionType.AUCTION_OPEN, plant=plant, bid=bid, discard=discard)

    @staticmethod
    def auction_bid_pass():
        """Create an action to pass during an active auction"""
        return PlayerAction(ActionType.AUCTION_BID_PASS)

    @staticmethod
    def auction_bid(bid, discard=None):
        """Create an action to bid in an active auction

        Args:
            bid: Bid amount
            discard: Card to discard if player has 3 plants
        """
        return PlayerAction(ActionType.AUCTION_BID, bid=bid, discard=discard)

    @staticmethod
    def resource_purchase(resources):
        """Create an action to purchase resources

        Args:
            resources: Dict of {resource_type: amount}, e.g., {'coal': 3, 'oil': 2}
        """
        return PlayerAction(ActionType.RESOURCE_PURCHASE, resources=resources)

    @staticmethod
    def city_build(cities):
        """Create an action to build in cities

        Args:
            cities: List of city names, e.g., ['Berlin', 'Paris']
        """
        return PlayerAction(ActionType.CITY_BUILD, cities=cities)

    @staticmethod
    def power_cities(power_plan):
        """Create an action to power cities

        Args:
            power_plan: Either:
                - int: Number of cities to power (engine picks plants greedily)
                - list: Detailed power plan with plant/resource specification
                    [{'plant': Card, 'resources': {'coal': 2}}, ...]
        """
        return PlayerAction(ActionType.POWER_CITIES, power_plan=power_plan)

    def __repr__(self):
        """String representation for debugging"""
        parts = [f"PlayerAction({self.action_type.value}"]

        if self.plant is not None:
            parts.append(f"plant={self.plant.cost}")
        if self.bid is not None:
            parts.append(f"bid={self.bid}")
        if self.discard is not None:
            parts.append(f"discard={self.discard.cost}")
        if self.resources:
            parts.append(f"resources={self.resources}")
        if self.cities:
            parts.append(f"cities={self.cities}")
        if self.power_plan is not None:
            parts.append(f"power_plan={self.power_plan}")

        return ", ".join(parts) + ")"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        result = {
            'action_type': self.action_type.value
        }

        if self.plant is not None:
            result['plant'] = self.plant.to_dict()
        if self.bid is not None:
            result['bid'] = self.bid
        if self.discard is not None:
            result['discard'] = self.discard.to_dict()
        if self.resources:
            result['resources'] = dict(self.resources)
        if self.cities:
            result['cities'] = list(self.cities)
        if self.power_plan is not None:
            if isinstance(self.power_plan, int):
                result['power_plan'] = self.power_plan
            else:
                # Detailed power plan with Card objects
                result['power_plan'] = [
                    {
                        'plant': plan['plant'].to_dict() if plan.get('plant') else None,
                        'resources': plan.get('resources')
                    }
                    for plan in self.power_plan
                ]

        return result
