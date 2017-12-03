# -*- coding: utf-8 -*-


import sys
from geopy.distance import great_circle, Point
from googlemaps.geocoding import geocode
from lxml import etree


def unique_id(store, store_id, chain_id=None):
    if chain_id:
        return "{}_{}_{}".format(store, chain_id, store_id)
    else:
        return "{}_{}".format(store, store_id)


def parse_price(xml, d, stores, store_name):
    chain_id = None
    for event, elem in etree.iterparse(xml, events=('end',)):
        if elem.tag.lower() == 'storeid':
            store_id = int(elem.text)
            sid = unique_id(store_name, store_id, chain_id)
            if sid not in stores:
                return
        if elem.tag.lower() == 'itemcode':
            barcode = elem.text
        if elem.tag.lower() == 'itemprice':
            price = float(elem.text)
        if elem.tag.lower() == 'line' or elem.tag.lower() == 'item' or elem.tag.lower() == 'product':
            d[barcode][sid].append(price)


def parse_promo(xml, d, stores, store_name):
    chain_id = None
    for event, elem in etree.iterparse(xml, events=('end',)):
        if elem.tag.lower() == 'storeid':
            store_id = int(elem.text)
            sid = unique_id(store_name, store_id, chain_id)
            if sid not in stores:
                return
        if elem.tag.lower() == 'itemcode':
            barcode = elem.text
        if elem.tag.lower() == 'discountedprice':
            price = float(elem.text)
        if elem.tag.lower() == 'minqty':
            min_qty = float(elem.text)
        if elem.tag.lower() == 'rewardtype':
            reward_type = int(elem.text)
        if elem.tag.lower() == 'line' or elem.tag.lower() == 'item' or elem.tag.lower() == 'sale':
            if reward_type == 1 or reward_type == 10:
                d[barcode][sid].append(price / min_qty)
                d[barcode][sid] = sorted(d[barcode][sid])
            elif reward_type == 7:
                if barcode in d and sid in d[barcode]:
                    d[barcode][sid].append((d[barcode][sid][-1] * min_qty - price) / min_qty)
                    d[barcode][sid] = sorted(d[barcode][sid])
            elif reward_type == 2 or reward_type == 3:
                d[barcode][sid].append(price)
                d[barcode][sid] = sorted(d[barcode][sid])
            elif reward_type == 8:
                if barcode in d and sid in d[barcode]:
                    d[barcode][sid].append(((min_qty - 1) * d[barcode][sid][-1] + price) / min_qty)
                    d[barcode][sid] = sorted(d[barcode][sid])


def get_geoloc(client, addr):
    for old, new in [(u'פינת', '&'), (u'אזו"ת', ''), (u'אזוה"ת', ''), (u"אזוה''ת", '')]:
        addr = addr.replace(old, new)
    loc = geocode(client, addr, language='iw')
    if len(loc) == 0:
        return None
    geoloc = loc[0]['geometry']['location']
    return Point(latitude=geoloc['lat'], longitude=geoloc['lng'])


def parse_stores(client, xml, store_name):
    root = etree.parse(open(xml))
    rv = {}
    chain_id = None
    for event, elem in etree.iterparse(xml, events=('end',)):
        if elem.tag.lower() == 'storeid':
            store_id = int(elem.text)
        if elem.tag.lower() == 'address':
            addr = elem.text
        if elem.tag.lower() == 'city':
            city = elem.text
            if not city or city in addr:
                city = ''
        if elem.tag.lower() == 'storename':
            store_name_attr = elem.text
        if elem.tag.lower() == 'line' or elem.tag.lower() == 'store' or elem.tag.lower() == 'branch':
            if (addr != 'unknown' and addr.strip() != '') or city.strip() != '':
                full_addr = u'{}, {}'.format(addr, city)
            else:
                full_addr = store_name_attr
            store_loc = get_geoloc(client, full_addr)
            if store_loc is None:
                print >> sys.stderr, 'Skipping store ', store_id
            else:
                rv[unique_id(store_name, store_id, chain_id)] = (store_loc, full_addr)
            store_id = -1
            addr = ''
            city = ''
    return rv


def fetch_stores(client, stores, src, max_distance):
    src_loc = get_geoloc(client, src)
    filtered = {}
    for key in stores.keys():
        p = Point(latitude=stores[key]['lat'], longitude=stores[key]['lon'])
        if great_circle(src_loc, p).kilometers < max_distance:
            filtered[key] = stores[key]
    return filtered