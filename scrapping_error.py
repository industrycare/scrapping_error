import re
import os
import csv
import datetime
import shutil, tempfile

per_error={}
directory = ['/home/ubuntu/mainservice/','/home/ubuntu/mailservice','/home/ubuntu/botservice','/home/ubuntu/reposervice','/home/ubuntu/simulationservice','/home/ubuntu/userauthservice_new']
datatime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

for x in range(len(directory)):
    
    for root, dirs, files in os.walk(directory[x]):
        for filename in files:
            if re.search(r".*(?=log$)",filename):
                file = os.path.join(root, filename)
                # print(file)
                with open(file, 'r') as text_file:
                        text_file=text_file.read()
                        error_geral = re.findall(r'(?P<timestamp>)(?P<errortype>[a-z]+Error:)+(?P<description>[\s\S]+?(?=\b[a-z][)]|$))', text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE )
                        error_broken = re.findall (r'(?P<timestamp>[a-zA-z]+\s[a-zA-z]+\s\s\d\s\d{2}:\d{2}:\d{2}\s\d{4})\s-\suwsgi_response_write_headers_do\(\):\s(?P<errortype>Broken pipe)+(?P<description>[\s\S]+?(?=\b[a-z][)]|$))', text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE)
                        error_server = re.findall(r'(?P<timestamp>)(?P<errortype>[a-z]+\s[a-z]+\sError:)+(?P<description>\s\/[a-z]+\/[a-z]+\/[a-z]+)',text_file, re.IGNORECASE | re.UNICODE | re.MULTILINE)
                        microservice = re.findall(r'(?P<microservice>(?s)(?s)(?<=\/ubuntu\/).*?(?=\/\b[a-z_]+\b))', file, re.IGNORECASE | re.UNICODE | re.MULTILINE )
                        # print(microservice)

                        for microservice in microservice:
                            for timestamp, errortype, description in error_geral:
                                per_error[ timestamp, errortype,description, microservice] = {
                                "microserviço": microservice,
                                "timestamp": datatime,
                                "tipoErro": errortype,
                                "descricao": description
                                
                            }

                            for timestamp, errortype, description in error_server:
                                per_error[ timestamp, errortype,description, microservice] = {
                                "microserviço": microservice,
                                "timestamp": datatime,
                                "tipoErro": errortype,
                                "descricao": description
                                }
                                    
                            for timestamp, errortype, description in error_broken:
                                per_error[ timestamp, errortype, description, microservice] = {
                                "microserviço": microservice,
                                "timestamp": datatime,
                                "tipoErro": errortype,
                                "descricao": description
                                } 

        #apenas para debbuging   
        for error_data in per_error.values():
            print(error_data) 

        #adiciona os erros encontrados no arquivo csv
        with open('errorlog.csv', 'a') as csvfile:
            fieldnames = [ "microserviço", "timestamp", "tipoErro", "descricao"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader() 
            for error_data in per_error.values():
                writer.writerow(error_data)   

        # move todo o conteúdo do "uwsgi_error.log" para o arquivo "uwsgi_error_permanente.log"
        if re.search(r"uwsgi_error.log",filename):  
            with open("uwsgi_error.log") as temporario:
                with open("uwsgi_error_permantente.log", "a") as permanente:
                    for line in temporario:
                        permanente.write(line)  

