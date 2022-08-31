import re
import os
import csv
import datetime
import json
import requests
import pandas as pd

dic_error={}
directory = ['/home/ubuntu/mainservice/','/home/ubuntu/mailservice','/home/ubuntu/botservice','/home/ubuntu/reposervice','/home/ubuntu/simulationservice','/home/ubuntu/userauthservice_new']

datatime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

for x in range(len(directory)):
    
    for root, dirs, files in os.walk(directory[x]):
        for filename in files:
            if re.search(r"uwsgi_error.log",filename):
                file = os.path.join(root, filename)
                with open(file, 'r') as text_file:
                        text_file=text_file.read()
                        error_geral = re.findall(r'(?P<timestamp>)(?P<errortype>[a-z]+Error:)+(?P<description>[\s\S]+?(?=\b[a-z][)]|$))', text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE )
                        error_broken = re.findall (r'(?P<timestamp>[a-zA-z]+\s[a-zA-z]+\s\s\d\s\d{2}:\d{2}:\d{2}\s\d{4})\s-\suwsgi_response_write_headers_do\(\):\s(?P<errortype>Broken pipe)+(?P<description>[\s\S]+?(?=\b[a-z][)]|$))', text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE)
                        error_server = re.findall(r'(?P<timestamp>)(?P<errortype>[a-z]+\s[a-z]+\sError:)+(?P<description>\s\/[a-z]+\/[a-z]+\/[a-z]+)',text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE)
                        microservice = re.findall(r'(?P<microservice>(?<=\/ubuntu\/).*?(?=\/\b[a-z_]+\b))', file, re.IGNORECASE | re.UNICODE | re.MULTILINE )


                        for microservice in microservice:
                            for timestamp, errortype, description in error_geral:
                                dic_error[ timestamp, errortype,description, microservice] = {
                                "microservice": microservice,
                                "timestamp": datatime,
                                "tipoErro": errortype,
                                "descricao": description
                                
                            }

                            for timestamp, errortype, description in error_server:
                                dic_error[ timestamp, errortype,description, microservice] = {
                                "microservice": microservice,
                                "timestamp": datatime,
                                "tipoErro": errortype,
                                "descricao": description
                                }
                                    
                            for timestamp, errortype, description in error_broken:
                                dic_error[ timestamp, errortype, description, microservice] = {
                                "microservice": microservice,
                                "timestamp": datatime,
                                "tipoErro": errortype,
                                "descricao": description
                                } 

        
#adiciona os erros encontrados no arquivo csv
with open('errorlog.csv', 'w') as csvfile:
    fieldnames = [ "microservice", "timestamp", "tipoErro", "descricao"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() 
    for error_data in dic_error.values():
        writer.writerow(error_data) 

#copia todo o conteúdo do "errorlog.csv" para o arquivo "errorlog_hist.csv" (para fins de histórico) 
with open("errorlog.csv") as temporario:
        with open("errorlog_hist.csv", "a") as permanente:
            for line in temporario:
                permanente.write(line)
 
# salvando arquivo json
csv_data = pd.read_csv("errorlog.csv", sep = ",")
csv_data.to_json("data.json", orient = "records", indent=4) 




    
