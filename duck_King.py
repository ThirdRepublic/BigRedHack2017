## requires lxml, beautifulsoup4
##http://www.cs.cornell.edu/courses/cs4410/2017fa/schedule/

import urllib2
from bs4 import BeautifulSoup

#url = raw_input("what site would you like to scrap? : ")

url = "http://www.cs.cornell.edu/courses/cs4410/2017fa/schedule/"

page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'lxml')

output = ""

headers = []
### Columns
col_headers = soup.find_all('th');
for i in col_headers:
    headers.append(i.text.strip())

rows = soup.find_all('tr')
for i in rows:
    columns = i.find_all('td')
    j = 0
    if(i.find(attrs={'class': 'week'})):
        print "\n" + headers[0] + " " + columns[0].text.strip()
        j = 1
    print columns[j].text.strip() + " " + columns[j+1].text.strip()
    k = 2
    while k <6:
        if(columns[j+k].text.strip()):
            print headers[k+1] + " " + columns[j+k].text.strip()
            if((columns[j+k].get("colspan"))):
                print headers[k+2] + " " + columns[j+k].text.strip()
                k+=(int)(columns[j+k].get("colspan"))
        k+=1

 
print "\n\nSchedule"
