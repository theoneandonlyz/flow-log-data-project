# Code by Zainub Ahmed

import csv

# Create new file for lookup table 
with open('lookup_table.csv', 'w') as lookup:
    header_names = ['dstport', 'protocol', 'tag']
    csv_writer = csv.DictWriter(lookup, fieldnames=header_names) 
    csv_writer.writeheader() 
    
# Create output file for tracking unique tags
with open('unique_tags.csv', 'w') as output1:
    header_names = ['Tag', 'Count']
    csv_writer = csv.DictWriter(output1, fieldnames=header_names) 
    csv_writer.writeheader() 
    
# Create output file for tracking unique port/protocol combinations
with open('port_protocol_combinations.csv', 'w') as output2:
    header_names = ['Port', 'Protocol', 'Count']
    csv_writer = csv.DictWriter(output2, fieldnames=header_names) 
    csv_writer.writeheader() 
    
# Reads CSV file, finds protocol name associated w/ protocol number
# CSV of protocol names are from the official IANA website
# https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml 
def find_protocol_name(protocol_num):
    protocol_name = 'undefined'
    with open('protocol-numbers-1.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # skip header line
        next(csv_reader)
        
        # parse through csv file for protocol name
        for line in csv_reader:
            if line[0] == protocol_num:
                protocol_name = line[1].lower()
                break
            
    return protocol_name


# Reads CSV file, finds service name based on port number and transport protocol name
# CSV of service names are from the official IANA website
# https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=3
def find_service_name(port_number, transport_protocol):
    service_name = None
    with open('service-names-port-numbers.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # skip header line
        next(csv_reader)
              
        # parse through csv file for service name/tag name
        for line in csv_reader:
            if line[1] == port_number and line[2].lower() == transport_protocol.lower():
                # print('Found it!')
                service_name = line[0].lower()
        
        # if service name is not found, assign name 'untagged'
        if service_name is None:
            service_name = 'untagged'
                    
    return service_name
        


def main():
    
    print(f'This program will parse through log file data')

    # define default sample log data to parse through
    default_file = "flow_logs.txt"

    # setup dictionaries for tracking results counters
    unique_tags = {}
    prt_pro_combinations = {}
    
    # ask user for input file name
    f = input("Please input file name: ")

    # check if input file name is empty
    if not f:
        f = default_file
        print(f"No file selected. Reading default file '{default_file}'")

    # open and read file
    try:
        with open(f, 'r') as file:
            
            for line in file:
                parts = line.strip().split()
                srcport = parts[5]
                dstport = parts[6]
                protocol_num = parts[7]
                
                # well-known ports range from 0 to 1023
                try:
                    if int(dstport) > 1023:
                        dstport = srcport
                except ValueError:
                    print("Error: dstport is not a valid integer")
                
                # find protocol and service names for lookup table
                protocol_name = find_protocol_name(protocol_num)
                service_name = find_service_name(dstport, protocol_name)
                # print(dstport, protocol_name, service_name)
                
                # add data to lookup_table.csv
                with open('lookup_table.csv', 'a') as lookup:
                    csv_writer = csv.writer(lookup)
                    row_data = [dstport, protocol_name, service_name]
                    csv_writer.writerow(row_data)
                    
                # uncomment to test 10000 mappints in the lookup_table.csv!
                # for i in range(10000):
                #     with open('lookup_table.csv', 'a') as lookup:
                #         csv_writer = csv.writer(lookup)
                #         row_data = [dstport, protocol_name, service_name]
                #         csv_writer.writerow(row_data)
                
                # update unique_tags dictionary
                tag_key = service_name
                if tag_key in unique_tags:
                    unique_tags[tag_key] += 1
                else:
                    unique_tags[tag_key] = 1
                    
                # update prt_pro_combinations dictionary
                combo_key = (dstport, protocol_name)
                if combo_key in prt_pro_combinations:
                    prt_pro_combinations[combo_key] += 1
                else:
                    prt_pro_combinations[combo_key] = 1
    except FileNotFoundError:
        print(f"Error: file '{f}' was not found. Reading default file '{default_file}'")
        try:
            with open(default_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    srcport = parts[5]
                    dstport = parts[6]
                    protocol_num = parts[7]
                    
                    # well-known ports range from 0 to 1023
                    try:
                        if int(dstport) > 1023:
                            dstport = srcport
                    except ValueError:
                        print("Error: dstport is not a valid integer")
                    
                    # find protocol and service names for lookup table
                    protocol_name = find_protocol_name(protocol_num)
                    service_name = find_service_name(dstport, protocol_name)
                    
                    # add data to lookup_table.csv
                    with open('lookup_table.csv', 'a') as lookup:
                        csv_writer = csv.writer(lookup)
                        row_data = [dstport, protocol_name, service_name]
                        csv_writer.writerow(row_data)
                        
                    # update unique_tags dictionary
                    tag_key = service_name
                    if tag_key in unique_tags:
                        unique_tags[tag_key] += 1
                    else:
                        unique_tags[tag_key] = 1
                        
                    # update prt_pro_combinations dictionary
                    combo_key = (dstport, protocol_name)
                    if combo_key in prt_pro_combinations:
                        prt_pro_combinations[combo_key] += 1
                    else:
                        prt_pro_combinations[combo_key] = 1
        except FileNotFoundError:
            print(f"Error: Default file '{default_file}' with sample log data was not found")
    except Exception as e:
        print(f"Error accessing file '{f}': '{e}'")

    
    # add data to unique_tags.csv
    with open('unique_tags.csv', 'a') as output1:
        csv_writer = csv.writer(output1)
        for key, value in unique_tags.items():
            row_data = [key, value]
            csv_writer.writerow(row_data)

    # add data to port_protocol_combinations.csv
    with open('port_protocol_combinations.csv', 'a') as output2:
        csv_writer = csv.writer(output2)
        for (port, protocol), count in prt_pro_combinations.items():
            row_data = [port, protocol, count]
            csv_writer.writerow(row_data)
    
if __name__ == "__main__":
    main()
