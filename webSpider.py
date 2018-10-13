import requests
import json
from bs4 import BeautifulSoup

if __name__ == '__main__':
     main()

def main():
     page_url = (
    "http://ca.healthinspections.us/napa/search.cfm?start=1&1=1&sd=01/01/1970&ed=03/01/2017&kw1=&kw2=&kw3="
    "&rel1=N.permitName&rel2=N.permitName&rel3=N.permitName&zc=&dtRng=YES&pre=similar"
)
    parse(page_url)

def parse(url):			
  jsonDic = {}				
  jsonIncrem = 0
  firstIncrem = 0
  secondIncrem = 0

  url = "https://ca.healthinspections.us/_templates/135/Food%20Inspection/_report_full.cfm?domainID=135&inspectionID=409588&dsn=dhd_135"

  sourceCode = requests.get(url)	
  plainText = sourceCode.text		
  soup = BeautifulSoup(plainText)

  for link in soup.findAll('span', {'class':'blackline'}):		
    firstIncrem += 1											
    information = link.string									
    
    if firstIncrem == 1:	
      facilityName = firstGetter(information, firstIncrem)		
      jsonDic[jsonIncrem] = (facilityName)						
    
    elif firstIncrem == 3:	
      jsonIncrem += 1											
      inspecDate = firstGetter(information, firstIncrem)		
      jsonDic[jsonIncrem] = (inspecDate)
    
    elif firstIncrem == 5:		
      streetDic = {}		
      cityDic = {}
      stateDic = {}
      zipCodeDic = {}			

      jsonIncrem += 1			
      locationContainer = firstGetter(information, firstIncrem)		

      streetAddress = locationContainer[0]				
      city = locationContainer[1]
      state = locationContainer[2]
      zipCode = locationContainer[3]

      streetDic["Street Address"] = streetAddress	
      jsonDic[jsonIncrem] = (streetDic)
      jsonIncrem += 1

      cityDic["City"] = city
      jsonDic[jsonIncrem] = (cityDic)
      jsonIncrem += 1

      stateDic["State"] = state
      jsonDic[jsonIncrem] = (stateDic)
      jsonIncrem += 1

      zipCodeDic["Zip Code"] = zipCode
      jsonDic[jsonIncrem] = (zipCodeDic)
      jsonIncrem += 1

    elif firstIncrem == 10:	
      jsonIncrem += 1
      inspecType = firstGetter(information, firstIncrem)
      jsonDic[jsonIncrem] = (inspecType)
    
  for link in soup.findAll('td', {'class':'center bold'}):
    secondIncrem += 1
    gradeDic = {}

    if secondIncrem == 2:
      jsonIncrem += 1
      inspecGrade = link.string

      gradeDic["Inspection Grade"] = inspecGrade[0]
      jsonDic[jsonIncrem] = (gradeDic)
      print(jsonDic)
  
  writeToJSON(jsonDic)

def firstGetter(info, increm): 
  if increm == 1:
    tempDic = {}      
    facilityName = info

    tempDic["Facility Name"] = facilityName
    return tempDic

  elif increm == 3:
    tempDic = {}  
    inspecDate = info

    tempDic["Inspection Date"] = inspecDate
    return tempDic

  elif increm == 5:
    badAddress = info
    
    streetAddress, temp_cityStateZip = badAddress.split(" \r\n")
    print(streetAddress + '\n')   
    print(temp_cityStateZip + '\n')

    city, temp_stateZip = temp_cityStateZip.split(", ")
    print(city + '\n')            
    print(temp_stateZip + '\n')

    state = temp_stateZip[:2]     
    zipCode = temp_stateZip[3:]   

    print(state + '\n')
    print(zipCode + '\n')

    tempContainer = [streetAddress, city, state, zipCode]

    return tempContainer

  elif increm == 10:
    tempDic = {}  
    inspecType = info
    tempDic["Inspection Type"] = inspecType
    return tempDic
	
def writeToJSON(data):
  file = open(r"# Add your directory here
               ", "w", encoding="UTF=8")
  json.dump(data, file, ensure_ascii=True)
  file.close()
