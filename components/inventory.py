import tcod as libtcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            text = 'You cannot carry any more, your inventory is full'
            results.append({
                'item_added': None,
                'message': Message(text, libtcod.yellow)
            })
        else:
            text = 'You pick up the {0}!'.format(item.name)
            results.append({
                'item_added': item,
                'message': Message(text, libtcod.blue)
            })

            self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            text = 'The {0} cannot be used'.format(item_entity.name)
            results.append({'message': Message(text, libtcod.yellow)})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(
                self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        text = 'You dropped the {0}'.format(item.name)
        results.append(
            {'item_dropped': item, 'message': Message(text, libtcod.yellow)})

        return results
