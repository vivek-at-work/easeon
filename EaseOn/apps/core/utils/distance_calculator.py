from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

def get_distance_in_meters(lat1_n,lon1_n,lat2_n,lon2_n):
    lat1 = radians(lat1_n)
    lon1 = radians(lon1_n)
    lat2 = radians(lat2_n)
    lon2 = radians(lon2_n)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance * 1000