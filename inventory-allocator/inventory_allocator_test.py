import unittest
from inventory_allocator import InventoryAllocator

class Test(unittest.TestCase):

  def test_happy_case(self):
    #exact inventory match
    order = { 'apple': 1 }
    inventory = [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]
    output = [{ 'owd': { 'apple': 1 } }]
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)

  def test_not_enough_inventory(self):
    #not enough inventory --> no allocations!
    order = { 'apple': 1 }
    inventory = [{ 'name': 'owd', 'inventory': { 'apple': 0 } }]
    output = []
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)


  def test_split_inventory(self):
    #split item across warehouses
    order = { 'apple': 10 }
    inventory = [{ 'name': 'owd', 'inventory': { 'apple': 5 } }, { 'name': 'dm', 'inventory': { 'apple': 5 } }]
    output = [{ 'owd': { 'apple': 5 } }, { 'dm': { 'apple': 5 } }]
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)

    #split order across warehouses, also tests that ites come from cheapest warehouse
    order = { 'apple': 5, 'orange': 6, 'pear': 7 }
    inventory = [{ 'name': 'owd', 'inventory': { 'apple': 5, 'pear': 7 } }, { 'name': 'dm', 'inventory': { 'pear': 3, 'orange': 6 } }]
    output = [{ 'owd': { 'apple': 5, 'pear': 7 } }, { 'dm': { 'orange': 6  } }]
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)

    #test more than two warehouses, splitting order across multiple warehouses
    order = { 'apple': 10, 'banana': 10, 'orange': 10, 'pear': 10 }
    inventory = [{ 'name': 'owd', 'inventory': { 'apple': 5, 'banana': 5 } }, { 'name': 'dm', 'inventory': { 'apple': 5, 'pear': 5 } }, { 'name': 'dwo', 'inventory': { 'orange': 10 } }, { 'name': 'md', 'inventory': { 'banana': 5, 'pear': 5 } }]
    output = [{ 'owd': { 'apple': 5, 'banana': 5 } }, { 'dm': { 'apple': 5, 'pear': 5 } }, { 'dwo': { 'orange': 10 } }, { 'md': { 'banana': 5, 'pear': 5 } }]
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)

  def test_empty_order(self):
    #order is empty
    order = {}
    inventory = [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]
    output = []
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)
  
  def test_empty_inventory(self):
    #no inventory, with keys
    order = { 'apple': 100 }
    inventory = [{'name': '', 'inventory': {  } }]
    output = []
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)

    #no inventory, empty dictionary
    order = { 'apple': 100 }
    inventory = [{}]
    output = []
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)

  def test_all_empty(self):
    #empty order and empty inventory
    order = {}
    inventory = []
    output = []
    inventory_allocation = InventoryAllocator(order, inventory)
    self.assertEqual(inventory_allocation.shipment_allocation(), output)

if __name__ == '__main__':
  unittest.main()