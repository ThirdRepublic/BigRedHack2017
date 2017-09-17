## requires lxml, beautifulsoup4
##http://www.cs.cornell.edu/courses/cs4410/2017fa/schedule/

from bs4 import BeautifulSoup
from googleCalendar import *

import googleCalendar
from datetime import datetime
#url = raw_input("what site would you like to scrap? : ")

def duck(url):

    soup = BeautifulSoup(url, 'lxml')
    return_list = []

    output = ""

    headers = []
    ### Columns
    col_headers = soup.find_all('th');
    for i in col_headers:
        headers.append(i.text.strip())


    rows = soup.find_all('tr')
    for i in rows:
        title = ""
        desc = ""
        dateStart = ''
        timeStart = '00:00:00'
        dateEnd = ''
        timeEnd = '00:00:00'
        isDefaultReminder = False
        emailHours = 48
        popupMinutes = 30

        columns = i.find_all('td')
        j = 0
        if(i.find(attrs={'class': 'week'})):
            #print "\n" + headers[0] + " " + columns[0].text.strip() disregard week #
            j = 1
        #print "\n" + columns[j].text.strip() + " " + columns[j+1].text.strip()
        # print "\n" + datetime.strptime(columns[j+1].text.strip() + ' 2017','%b %d %Y').strftime("%Y-%m-%d")
        dateStart = datetime.strptime(columns[j+1].text.strip() + ' 2017','%b %d %Y').strftime("%Y-%m-%d")
        dateEnd = datetime.strptime(columns[j+1].text.strip() + ' 2017','%b %d %Y').strftime("%Y-%m-%d")
        k = 2
        while k <6:
            if(columns[j+k].text.strip()):
                # print headers[k+1] + ": " + columns[j+k].text.strip(),
                title += headers[k+1] + ": " + columns[j+k].text.strip() + " "
                desc += headers[k+1] + ": " + columns[j+k].text.strip() + " "
                if(columns[j+k].find('a')):
                    # print "http://www.cs.cornell.edu/" + columns[j+k].find('a').get("href")
                    title += "http://www.cs.cornell.edu/" + columns[j+k].find('a').get("href") + " "
                    desc += "http://www.cs.cornell.edu/" + columns[j+k].find('a').get("href") + " "
                #else:
                    # print
                if((columns[j+k].get("colspan"))):
                    # print headers[k+2] + " " + columns[j+k].text.strip()
                    title += headers[k+2] + " " + columns[j+k].text.strip() + " "
                    desc += headers[k+2] + " " + columns[j+k].text.strip() + " "
                    k+=(int)(columns[j+k].get("colspan"))
            k+=1

        return_list.append((desc, dateStart))
        #appendEvent(title,desc,dateStart,timeStart,dateEnd,timeEnd,isDefaultReminder,emailHours,popupMinutes)

    # appendEvent("Google I/O 2015","A chance to hear more about Google\'s developer products.",'2017-09-18','06:00:00','2017-09-18','10:00:00',False,48,30)
    return return_list