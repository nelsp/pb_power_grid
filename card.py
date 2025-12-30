class Card:
  def __init__(self, props):
    self.cost = props.get('cost')
    self.resource = props.get('resource')
    self.resource_cost = props.get('resource_cost')
    self.cities = props.get('cities')
    self.type = props.get('type') or 'light'
    
    # change to dark card if necessary
    if self.cost < 16:
      self.type = 'dark'
  
  def __repr__(self):
    return """
    ##########################
            Cost {}                 
                            
          {} {} ==> {}
           Type: {}           
    ##########################
    """.format(self.cost, self.resource_cost, self.resource, self.cities, self.type)