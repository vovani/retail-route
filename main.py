# -*- coding: utf-8 -*-

import json
import os
import numpy as np

from googlemaps.client import Client
from glob import glob
from collections import defaultdict
from lxml import etree

from parse import parse_stores, fetch_stores, parse_price, parse_promo, unique_id
from route import find_route, cheapest


if __name__ == '__main__':
    dir = '/mnt/c/Work/PharmTraverse/Data'
    ff = glob(dir + '/*/*.xml')
    prices_filenames = np.array(filter(lambda f: 'price' in f.lower(), ff))
    promos_filenames = filter(lambda f: 'promo' in f.lower(), ff)
    store_filenames = filter(lambda f: 'store' in f.lower(), ff)
    print len(prices_filenames)
    print len(promos_filenames)
    print len(store_filenames)
    c = Client(key='AIzaSyBsOohh5S08mhOmKT00ncWtFUBJXddhRvg')
    if os.path.exists('/mnt/c/Work/PharmTraverse/Data/stores.json'):
        stores_raw = json.load(open('/mnt/c/Work/PharmTraverse/Data/stores.json'))
    else:
        stores_raw = {}
        for store_filename in store_filenames:
            store_name = os.path.basename(os.path.dirname(store_filename))
            print store_filename
            print store_name
            new_stores = parse_stores(c, store_filename, store_name)
            stores_raw.update({sid: {'lat': p[0].latitude, 'lon': p[0].longitude, 'addr': p[1]}
                      for sid, p in new_stores.items()})
        json.dump(stores_raw, open('/mnt/c/Work/PharmTraverse/Data/stores.json', 'wb'))
    stores = fetch_stores(c, stores_raw, u'מהר"ל, תל אביב', 10)

    if os.path.exists('/mnt/c/Work/PharmTraverse/Data/prices.json'):
        d = json.load(open('/mnt/c/Work/PharmTraverse/Data/prices.json'))
    else:
        d = defaultdict(lambda: defaultdict(list))
        for f in prices_filenames:
            store_name = os.path.basename(os.path.dirname(f))
            parse_price(open(f), d, stores, store_name)
        for f in promos_filenames:
            store_name = os.path.basename(os.path.dirname(f))
            parse_promo(open(f), d, stores, store_name)
        json.dump(d, open('/mnt/c/Work/PharmTraverse/Data/prices.json', 'wb'))

    print find_route((32.113441, 34.801411), 100, 10, d['5099864006704'], stores)
    # print map(lambda store_id: stores[store_id], route)

    import ipdb; ipdb.set_trace()
    # prices = [float(etree.parse(open(f)).xpath('//ItemCode[text()=5099864006704]/../ItemPrice/text()')[0])
    #           for f in prices_filenames]
    prices = np.array(prices)
    print prices.argmin(), prices.min(), prices.argmax(), prices.max(), prices.mean(), np.median(prices)
    args = np.argsort(prices)
    print zip(prices_filenames[args[:10]], prices[args[:10]])
    print '-------------------------------'
    print zip(prices_filenames[args[-10:]], prices[args[-10:]])
    print 'Loaded prices'
    promos = [etree.parse(open(f)).xpath('//ItemCode[text()=5099864006704]/../PromotionDetails/DiscountedPrice/text()')
              for f in promos_filenames]
    print 'Loaded Promos'
    prices = np.array(prices)
    print zip(promos, promos_filenames)
    import ipdb; ipdb.set_trace()