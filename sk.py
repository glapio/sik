import subprocess
import time
import re
import random
import string
 
# Define the protocols, packet sizes, and file lengths to test
protocols = ['tcp']
, 'udp', 'udpr']
packet_sizes = [512,1024,8192,16384,32768,64000]
file_lengths = [1024,10240,102400,102400,1024000,10240000]
 
# Define the IP host and port
ip_host = '192.168.42.25'
port = '60123'
 
# Loop over the protocols, packet sizes, and file lengths
for protocol in protocols:
    for packet_size in packet_sizes:
        for file_length in file_lengths:
            # Change the values in size_const.h
            with open('size_const.h', 'r') as file:
                filedata = file.read()
            filedata = re.sub(r'#define MAX_DATA_SIZE \d+', f'#define MAX_DATA_SIZE {packet_size}', filedata)
            
            with open('size_const.h', 'w') as file:
                file.write(filedata)
 
            # Compile the program
            subprocess.run(['make', 'all'], check=True)
 
            # Generate a random string of data of the appropriate size
            data = ''.join(random.choices(string.ascii_letters + string.digits, k=file_length * 1024))
 
            # Run the program and measure the execution time
            start_time = time.time()
            command = ['./ppcpc', protocol, ip_host, port]
            p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p.communicate(input=data.encode())[0]
            end_time = time.time()
 
            # Print the results
            print(f'Protocol: {protocol}, Packet size: {packet_size}, File length: {file_length}, Time: {end_time - start_time}, Output: {output.decode()}')
