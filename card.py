class Card:
  def __init__(self, props):
    self.cost = props.get('cost')
    self.resources = props.get('resources')
    self.resource_cost = props.get('resource_cost')
    self.cities = props.get('cities')
    self.type = props.get('type')
  
  def __repr__(self):
		return """
		##########################
		        Cost {}                 
		                        
		      {} {} ==> {}
		       Type: {}           
		##########################
		""".format(self.cost, self.resource_cost, self.resource, self.cities, self.type)