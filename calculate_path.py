import pandas as pd
from math import radians, cos, sin, asin, sqrt
import numpy as np
from collections import defaultdict
import sys

def haversine(lon1,lat1,lon2,lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    R=6371
    return c * R

def read_dataset(filename):
    dataset = pd.read_csv(filename,header=None).as_matrix()
    return dataset

def compute_lat_lon_tup(dataset):
    lat_long_tup =[]
    for i in range(0,len(dataset)):
        tup=(dataset[i][0],dataset[i][1])
        lat_long_tup.append(tup)
    return lat_long_tup


def get_lat_long_tup_with_dist(lat_long_tup,origin_lat,origin_lon):
    lat_long_tup_with_dist=[]
    for i,v in enumerate(lat_long_tup):
        dist = haversine(origin_lon,origin_lat,v[1],v[0])
        lat_long_tup_with_dist.append([i,dist])
    return lat_long_tup_with_dist

def compute_dist_matrix(lat_long_tup,origin_lat,origin_lon):
    dist_pair={}
    for i in range(0,len(lat_long_tup)):
        for j in range(i+1,len(lat_long_tup)):
            dist_pair[(i,j)]=haversine(lat_long_tup[i][1],lat_long_tup[i][0],lat_long_tup[j][1],lat_long_tup[j][0])
    for i in range(0,len(lat_long_tup)):
        dist_pair[(-1,i)]=haversine(lat_long_tup[i][1],lat_long_tup[i][0],origin_lon,origin_lat)
    return dist_pair

def get_route(sorted_latlon_tup_with_dist,drivers,dist_pair,drivers_score):
    visited_nodes=[]
    while True:
        if len(visited_nodes)==len(sorted_latlon_tup_with_dist):
            break
        minimum_dist = 1e6
        for i in range(0,len(sorted_latlon_tup_with_dist)):
            curr_loc = sorted_latlon_tup_with_dist[i][0]
            if curr_loc not in visited_nodes:
                for j in range(0,len(drivers)):
                    driver_loc = drivers[j][-1]
                    if driver_loc < curr_loc:
                        dist = dist_pair[(driver_loc,curr_loc)] + drivers_score[j]
                    else:
                        dist = dist_pair[(curr_loc,driver_loc)] + drivers_score[j]
                    if dist < minimum_dist:
                        minimum_dist=dist
                        new_curr_loc = curr_loc
                        driver_index = j
        drivers[driver_index].append(new_curr_loc)
        visited_nodes.append(new_curr_loc)
        drivers_score[driver_index]=minimum_dist
        if len(visited_nodes)%200==0:
            print "Number of nodes processed %s" %(len(visited_nodes))
    return drivers

def write_output(lat_long_tup,drivers,outputfile):
    f = open(outputfile,"w+")
    for i,v in enumerate(lat_long_tup):
        for j in range(0,len(drivers)):
            if i in drivers[j]:
                indx = drivers[j].index(i)
                f.write(str(v[0])+","+str(v[1])+","+str(j)+","+str(indx)+"\n")
                break
    f.close()
                

def main():
    num_drivers = int(sys.argv[1])
    origin_lat = float(sys.argv[2])
    origin_lon = float(sys.argv[3])
    input_file = sys.argv[4]
    output_file = sys.argv[5]


    dataset=read_dataset(input_file)
    lat_long_tup=compute_lat_lon_tup(dataset)

    lat_long_tup_with_dist=get_lat_long_tup_with_dist(lat_long_tup,origin_lat,origin_lon)
    sorted_latlon_tup_with_dist = sorted(lat_long_tup_with_dist,key=lambda x:x[1],reverse=False)

    dist_pair = compute_dist_matrix(lat_long_tup,origin_lat,origin_lon)

    drivers=defaultdict(list)
    for i in range(0,num_drivers):
        drivers[i].append(-1)
    
    drivers_score={}
    for i in range(0,num_drivers):
        drivers_score[i]=0.0
    drivers = get_route(sorted_latlon_tup_with_dist,drivers,dist_pair,drivers_score)

    write_output(lat_long_tup,drivers,output_file)




if __name__=="__main__":
    main()
