from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import QueryDict
import simplejson as json
from pymongo import MongoClient
import datetime
import traceback
import os


DEFAULT_POLYGON = '[[77.6254071, 12.939884], [77.6255329, 12.9399961], [77.6256759, 12.9401489]]'


def home(request):
    id = request.GET.get('id', None)
    coords = request.GET.get('coords', '12.9385113,77.6230193,17')
    try:
        coords = coords.split(',')
        lat = coords[0]
        lng = coords[1]
        zoom = coords[2]
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.autolocations
        place = request.GET.get('place', 'Koramangala, Bengaluru')
        if id:
            loc = locations.find_one({'gid': id},
                                     {'gid': True, 'name': True, 'polygon': True, 'polyauto': True})
            place_lvl1 = loc['name']
        else:
            place = [s.strip() for s in place.split(',')]
            place_lvl1 = place[0]
            place_lvl2 = place[1]
            # TODO: Location count logic inside Mongo query:
            if locations.count({'name': place_lvl1}) > 1:
                loc = locations.find_one({'name': {'$in': [place_lvl1, '{0}, {1}'.format(place_lvl1, place_lvl2)]},
                                          '$or': [{'place_type': 'city', 'city_name': place_lvl2}, {'hierarchy': {'$elemMatch': {'$elemMatch': {'name': {'$in': place[1:]}}}}}]},
                                         {'gid': True, 'polygon': True, 'polyauto': True})
            else:
                loc = locations.find_one({'name': place_lvl1},
                                         {'gid': True, 'polygon': True, 'polyauto': True})
        if 'polyauto' in loc and loc['polyauto']:
            polygon = loc['polyauto']
        else:
            polygon = loc['polygon']
    except:
        place_lvl1 = 'Koramangala'
        lat = 12.933221
        lng = 77.6321925
        zoom = 14
        polygon = DEFAULT_POLYGON
        traceback.print_exc()
    finally:
        client.close()
    return render_to_response('index.html', {'id': loc['gid'], 'place': place_lvl1, 'lat': lat, 'lng': lng, 'zoom': zoom, 'polygon': []})


def get_next_polygon(request):
    resp = HttpResponse()
    place = request.GET.get('place', '')
    not_id = request.GET.get('notId', '')
    try:
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.locations
        loc = locations.find_one({'name': place, 'gid': {'$ne': not_id}},
                                 {'gid': True, 'polygon': True, 'polyedit': True, 'updated': True, 'alreadyCorrect': True, 'openedForEdit': True})
        if loc:
            if 'polyedit' in loc:
                polygon = loc['polyedit']
            else:
                polygon = loc['polygon']
            resp = HttpResponse(json.dumps({'id': loc['gid'], 'polygon': polygon}, indent=4))
    except:
        traceback.print_exc()
    finally:
        client.close()
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def save_polygon(request):
    resp = HttpResponse(status=200)
    put = QueryDict(request.body)
    id = put.get('id', '')
    polygon = put.get('polygon', DEFAULT_POLYGON)
    try:
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.locations
        locations.update_one({'gid': id}, {'$set': {'polyedit': json.loads(polygon), 'updated': True}})
    except:
        traceback.print_exc()
        resp = HttpResponse(status=500)
    finally:
        client.close()
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def save_vertex(request):
    resp = HttpResponse(status=200)
    put = QueryDict(request.body)
    id = put.get('id', '')
    coords = put.get('coords', None)
    try:
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.autolocations
        locations.update_one({'gid': id}, {'$set': {'polyauto': json.loads(coords)}})
    except:
        traceback.print_exc()
        resp = HttpResponse(status=500)
    finally:
        client.close()
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def reset(request):
    polygon = DEFAULT_POLYGON
    put = QueryDict(request.body)
    id = put.get('id', '')
    try:
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.locations
        loc = locations.find_one({'gid': id}, {'polygon': True, 'updated': True, 'manualNav': True})
        polygon = loc['polygon']
        locations.update_one({'gid': id}, {'$set': {'polyedit': polygon}})
        if 'updated' in loc and loc['updated']:
            locations.update_one({'gid': id}, {'$set': {'updated': False}})
        if 'manualNav' in loc and loc['manualNav']:
            locations.update_one({'gid': id}, {'$set': {'manualNav': False}})
    except:
        traceback.print_exc()
    finally:
        client.close()
    resp = HttpResponse(json.dumps(polygon, indent=4))
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def get_next_place(request):
    resp = HttpResponse()
    try:
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.autolocations
        loc = locations.find_one({'polygon': {'$exists': True}, 'name': 'Koramangala'},
                                 {'gid': True, 'name': True, 'hierarchy': True})
        if len(loc['hierarchy']) > 0 and len(loc['hierarchy'][0]) > 0:
            place = ', '.join([lvl['name'] for lvl in loc['hierarchy'][0]])
        else:
            place = loc['name']
        resp = HttpResponse(json.dumps({'id': loc['gid'], 'place': place}, indent=4))
    except:
        traceback.print_exc()
    finally:
        client.close()
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def get_next_place_chrome(request):
    resp = HttpResponse()
    try:
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.locations
        loc = locations.find_one({'$and': [{'newZoom': {'$exists': True}}, {'newZoom': None}]},
                                 {'gid': True, 'name': True, 'city_name': True, 'hierarchy': True, 'manualNav': True, 'googlePlace': True})
        # locations.update_one({'gid': loc['gid']}, {'$set': {'snapped': True}})
        if 'manualNav' in loc and loc['manualNav']:
            place = loc['googlePlace']
        # gid: '1984884462b2beef955ca762503b1df6' - Eklahare for example will not come unless concatenated with city (Pune).
        elif 'hierarchy' in loc and len(loc['hierarchy']) > 0 and len(loc['hierarchy'][0]) > 0:
            place = ', '.join([lvl['name'] for lvl in loc['hierarchy'][0]])
        else:
            place = loc['name']
        resp = HttpResponse(json.dumps({'id': loc['gid'], 'city': loc['city_name'], 'place': place}, indent=4))
    except:
        traceback.print_exc()
    finally:
        client.close()
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def upload_image(request):
    try:
        id = request.GET.get('id', None)
        coords = request.GET.get('coords', None).split(',')
        lng = float(coords[1])
        lat = float(coords[0])
        zoom = int(coords[2])
        client = MongoClient("mongodb://localhost:27017")
        locations = client.test.locations
        loc = locations.find_one({'gid': id}, {'center': True})
        print(lng, lat, zoom, id)
        print(loc)
        if loc:
            if 'center' in loc:
                mon_lng = loc['center'][0]
                mon_lat = loc['center'][1]
                if lng != mon_lng or lat != mon_lat:
                    locations.update_one({'gid': id}, {'$set': {'newCenter': [lng, lat], 'newZoom': zoom}})
            else:
                locations.update_one({'gid': id}, {'$set': {'newZoom': zoom}})
    except:
        traceback.print_exc()
    resp = HttpResponse()
    resp['Access-Control-Allow-Origin'] = "*"
    return resp