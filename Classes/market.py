class Market:
  def __init__(self, cards):
    self.active_market = cards[:4]
    self.inactive_market = cards[4:]
  
  def purchase_card(self, index_purchased_card, card_to_add):
    """ Purchase a card from the active market and add a new card to the market"""
    pass
  
  