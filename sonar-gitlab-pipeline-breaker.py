#!/usr/local/bin/python3
import sys
import urllib.request, json 

def main():
 projectid = sys.argv[1]
 sonarurl = "https://sonar.example.com/api/qualitygates/project_status?projectKey=" + str(projectid) 
 with urllib.request.urlopen(sonarurl) as url:
    data = json.loads(url.read().decode())
    quality_gate_result = (data['projectStatus']['status'])
 if quality_gate_result == "OK":
    exit(0)
 else:
    exit(1)

if __name__ == '__main__':
    main()