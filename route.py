import numpy as np
from geopy.distance import great_circle, Point

def find_route(src, qty, max_per_store, store2price, store_locs):
    store_locs = {k: Point(latitude=v['lat'], longitude=v['lon']) for k, v in store_locs.items()}
    keys = store_locs.keys()
    keys = filter(lambda store: store in store2price, keys)
    acquired = 0
    current_loc = src
    route = []
    while acquired < qty:
        prices = np.array(map(lambda store: store2price[store][0], keys))
        distances = np.array(map(lambda store: great_circle(current_loc, store_locs[store]).kilometers, keys))
        distances_home = np.array(map(lambda store: great_circle(src, store_locs[store]).kilometers, keys))
        going_to_purchase = min(max_per_store, qty - acquired)
        score = going_to_purchase * prices + 0.5 * (distances + distances_home)
        best = np.argmin(score)
        print prices[best]
        acquired += going_to_purchase
        current_loc = store_locs[keys[best]]
        route.append(keys[best])
        keys.remove(keys[best])
    return route


def cheapest(prices, barcode, stores):
    store2price = prices[barcode].items()
    store2price = filter(lambda item: item[0] in stores, store2price)
    store2price.sort(key=lambda item: item[1][0])
    return store2price
#
# def find_route2(src, qty, max_per_store, store2price, store_locs):
#     store_locs = {k: Point(latitude=v['lat'], longitude=v['lon']) for k, v in store_locs.items()}
#     keys = store_locs.keys()
#     acquired = 0
#     current_loc = src
#     route = [0, 0]
#     while acquired < qty:
#         for i in xrange(len(route)):
#             prices = np.array(map(lambda store: store2price[store][0], keys))
#             distances_from = np.array(map(lambda store: great_circle(, store_locs[store]).kilometers, keys))
#             distances_home = np.array(map(lambda store: great_circle(src, store_locs[store]).kilometers, keys))
#             going_to_purchase = min(max_per_store, qty - acquired)
#             score = going_to_purchase * prices + 0.5 * (distances + distances_home)
#             best = np.argmin(score)
#             acquired += going_to_purchase
#             current_loc = store_locs[keys[best]]
#             route.append(keys[best])
#             keys.remove(keys[best])
#     return route
