import json
import csv
from csv import reader
def create_feature_dict(location_record):
    """ Takes in a location record as a list and returns it as a dictionary to be appended to the features_list """
    return_dict = {"type":"Feature"}
    
    record_dict = {}
    
    record_dict["C"] = location_record[0]
    record_dict["E"] = location_record[5]
    record_dict["SV"] = location_record[6]
    record_dict["SA"] = location_record[7]
    if coop_record[9] != '':
        record_dict["D"] = location_record[9]
    
    return_dict["properties"] = record_dict
    return_dict["geometry"] = {"type":"Point","coordinates":[float(location_record[2]),float(location_record[1])]}
    
    return return_dict
def create_geojson(csv_file_open_path, file_save_path_name):
    """ Creates a geojson from csv file """
    data = []
    with open(csv_file_open_path,'r') as f:
        reader = csv.reader(f)
        for record in reader:
            data.append(record)

    data = data[1::]
    
    for record in data:
        # shorten latitude to 4 decimal places
        lat = record[1].split('.')
        lat_diff = len(lat[1])-4
        lat[1] = lat[1][0:len(lat[1])-lat_diff]
        record[1] = float(lat[0] + '.' + lat[1])
        
        # shorten longitude to 4 decimal places
        long = record[2].split('.')
        long_diff = len(long[1])-4
        long[1] = long[1][0:len(long[1])-long_diff]
        record[2] = float(long[0] + '.' + long[1])
        
        record[4] = record[4].replace(',', ', ')
        record[7] = record[7].replace(',', ', ')
    
    data_file = {"type": "FeatureCollection"}
    data_file["crs"] = {"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}
    features_list = []
    
    for coop in data:
        features_list.append(create_feature_dict(coop))
        
    data_file["features"] = features_list
    
    with open(file_save_path_name, 'w') as ff:
        ff.write(json.dumps(data_file))

create_geojson('example.csv', 'final.geojson')
