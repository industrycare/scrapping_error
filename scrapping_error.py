import re
import os
import csv

per_error={}
directory = '/home/ubuntu/'

for root, dirs, files in os.walk(directory):
    for filename in files:
        if re.search(r".*(?=log$)",filename):
            file = os.path.join(root, filename)
            print(file)
            with open(file, 'r') as text_file:
                    text_file=text_file.read()
                    error_geral = re.findall(r'(?P<timestamp>)(?P<errortype>[a-z]+Error:)+(?P<description>[\s\S]+?(?=\b[a-z][)]|$))', text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE | re.MULTILINE)
                    error_broken = re.findall (r'(?P<timestamp>[a-zA-z]+\s[a-zA-z]+\s\s\d\s\d{2}:\d{2}:\d{2}\s\d{4})\s-\suwsgi_response_write_headers_do\(\):\s(?P<errortype>Broken pipe)+(?P<description>[\s\S]+?(?=\b[a-z][)]|$))', text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE)
                    error_server = re.findall(r'(?P<timestamp>)(?P<errortype>[a-z]+\s[a-z]+\sError:)+(?P<description>\s\/[a-z]+\/[a-z]+\/[a-z]+)',text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE)

                    for timestamp, errortype, description in error_geral:
                        per_error[timestamp, errortype,description] = {
                            "timestamp": None,
                            "tipoErro": errortype,
                            "descricao": description    
                        }

                    for timestamp, errortype, description in error_server:
                        per_error[timestamp, errortype,description] = {
                            "timestamp": None,
                            "tipoErro": errortype,
                            "descricao": description
                        }
                        
                    for timestamp, errortype, description in error_broken:
                        per_error[timestamp, errortype, description] = {
                            "timestamp": timestamp,
                            "tipoErro": errortype,
                            "descricao": description
                        }

                   
        for error_data in per_error.values():
            print(error_data) 

        with open('errorlog.csv', 'a') as csvfile:
            fieldnames = [ "timestamp", "tipoErro", "descricao"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader() 
            for error_data in per_error.values():
                writer.writerow(error_data)   