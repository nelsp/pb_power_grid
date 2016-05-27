class Resource:
  def __init__(self, props):
    self.type = props.get('type')
    self.cost = props.get('cost')