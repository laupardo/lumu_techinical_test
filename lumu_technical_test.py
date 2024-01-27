#!/usr/bin/env python
import re
from collections import Counter
from datetime import datetime
import requests
import json
import sys

def parse_bind9_log(log_file_path):
    log_entries = []
    with open(log_file_path, 'r') as file:
        for line in file:
            #Regex that matches log format
            pattern = r'(\d+-\w+-\d+ \d+:\d+:\d+\.\d+) queries: info: client @\S+ (\S+)#(\d+) \((\S+)\): query: (\S+) (\S+) (\S+)'
            match = re.search(pattern, line)

            if match:
                timestamp, client_ip, client_port, host, query, query_class, query_type = match.groups()
                log_entries.append({
                   'timestamp': timestamp,
                    'client_ip': client_ip,
                    'client_port': client_port,
                    'host': host,
                    'query': query,
                    'query_class': query_class,
                    'query_type': query_type
                })

    return log_entries

def convert_timestamp(original_timestamp):
    # Convert original timestamp to a datetime object
    dt_object = datetime.strptime(original_timestamp, "%d-%b-%Y %H:%M:%S.%f")
    # Format the datetime object to new format
    formatted_timestamp = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return formatted_timestamp

def get_fields(entry):
    #client_name is not specified in the requirement and it is optional, I will not be using that
    return {
        'timestamp': convert_timestamp(entry['timestamp']),
        'name': entry['host'],
        'client_ip': entry['client_ip'],
        'type': entry['query_type']
    }
def format_list_for_endpoint(previous_list):
    #endpoint asks for a different timestamp format and does not use the same variable names or amount of variables extracted
    new_list = [get_fields(entry) for entry in previous_list]
    return new_list

def send_data_to_endpoint(old_entries):
    entries = format_list_for_endpoint(old_entries)
    #these should be env variables but for the sake of this demo they will be plain
    lumu_client_key = 'd39a0f19-7278-4a64-a255-b7646d1ace80'
    collector_id ='5ab55d08-ae72-4017-a41c-d9d735360288'
    url = f'https://api.lumu.io/collectors/{collector_id}/dns/queries?key={lumu_client_key}'
    chunk_size = 500
    for chunk in get_chunk_list(entries, chunk_size):
        res = requests.post(url=url,data=json.dumps(chunk))

def get_chunk_list(list_to_chunk, chunk_size):
    #yield is less memory intensive
    for i in range(0, len(list_to_chunk), chunk_size):
        yield list_to_chunk[i:i + chunk_size]

if __name__ == "__main__":
    log_path = sys.argv[1]
    entries = parse_bind9_log(log_path)
    #send data to endpoint
    send_data_to_endpoint(entries)
    #number of entries part
    number_entries = len(entries)
    print(f'Total records: {number_entries}')
    #client IPs part
    print('\nClient IPs Rank')
    print('\n---------------- ---- -------')
    client_ips_counter = Counter(entry['client_ip'] for entry in entries)
    #use most_common() to sort from highest occurence to lowest
    for ip, count in client_ips_counter.most_common():
        percentage = (count / number_entries) * 100
        print(f'{ip:<16} {count:<5} {percentage:.2f}%')
    print('\n---------------- ---- -------')
    #host rank part
    print('\nHost Rank')
    print('------------------------------------------------------------ ---- -------')
    host_count = Counter(entry['host'] for entry in entries)
    for host, count in host_count.most_common():
        percentage = (count / number_entries) * 100
        print(f'{host:<60} {count:<5} {percentage:.2f}%')

