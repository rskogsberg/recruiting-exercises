class InventoryAllocator():

  def __init__(self, order, inventory):

    self.order = order

    self.inventory = inventory

  def shipment_allocation(self):
    #if either the inventory or order is empty, return []
    if not self.inventory or not self.order:

      return []
    #return [] if the order or inventory is an empty dictionary
    elif self.order == {} or self.inventory == [{}]:

      return []

    else:
      #make a copy of the order and inventory
      order_tracker = self.order
      warehouses = self.inventory

      #initialize the shipment
      shipment = []

      #iterate over warehouses to ensure cheapest allocation
      for warehouse in warehouses:

        #create map of items which can be shipped from 
        can_ship = {}

        #check for each item in the order
        for key in order_tracker:

          #check if item still needs to be fulfilled
          if order_tracker[key] > 0:

            #check that item exists in current warehouse, prevent key error
            if key in warehouse['inventory']:

              #conditional for when warehouse has enough inventory to fulfill order
              if warehouse['inventory'][key] > order_tracker[key]:
                
                #update what can be shipped from this warehouse with order value
                can_ship[key] = order_tracker[key]

                #update warehouse inventory with removed item
                warehouse['inventory'][key] = warehouse['inventory'][key] - order_tracker[key]

                #set order tracker to 0 because order quantity has been fulfilled
                order_tracker[key] = 0

              #conditional for when warehouse does not have enough inventory to fulfill order
              else:
                
                #update shipping information with the amount that the given warehouse can fulfill
                can_ship[key] = warehouse['inventory'][key]

                #update order tracker with original value less the amount the previous warehouse(s) was able to fulfill
                order_tracker[key] = order_tracker[key] - warehouse['inventory'][key]

                #set warehouse inventory for current item to 0, as order was large than inventory
                warehouse['inventory'][key] = 0

        #update shipment information with details for what each warehouse can fulfill
        shipment.append({warehouse['name']: can_ship})

      #check each item in the order to ensure every item was able to be fulfilled
      for key in order_tracker:

        #if any item has not been fulfilled return []
        if order_tracker[key] > 0:

          return []
      
    #update inventory with information f
    self.inventory = warehouses

    return shipment