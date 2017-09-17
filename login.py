#!/usr/bin/python
# Melik Yuksel

import requests
import lxml.html
import csv

def cms(url, username, password):
  s = requests.session()

  login = s.get('https://cmsx.cs.cornell.edu/web/auth/?action=loginview')
  form = {}

#  print "Login URL:", login.url, "\n"

  form['netid'] = username
  form['password'] = password

  response = s.post(login.url, data=form)
#  print "Response URL:", response.url, "\n"
  response_html = lxml.html.fromstring(response.text)
  response_form = response_html.xpath(r'//form[@name="bigpost"]')

  back_url = response_form[0].attrib['action']
  back_key = response_html.xpath(r'//form//input[@name="wa"][@type="hidden"]')[0].attrib['value']
  back_form = {'wa': back_key}

  back_response = s.post(back_url, data=back_form)

  r2 = s.get(url)
#  print "Page load URL:", r2.url, "\n"
#  print r2.text

  return r2.text

def blackboard(url, username, password):
  s = requests.session()

  login = s.get('https://blackboard.cornell.edu/webapps/bb-auth-provider-shibboleth-bb_bb60/execute/shibbolethLogin?returnUrl=https%3A%2F%2Fblackboard.cornell.edu%2Fwebapps%2Fportal%2Fexecute%2FdefaultTab&authProviderId=_5555_1')
  form = {}

  #print "Login URL:", login.url, "\n"

  form['netid'] = username
  form['password'] = password

  response = s.post(login.url, data=form)
  #print "Response URL:", response.url, "\n"
  response_html = lxml.html.fromstring(response.text)
  response_form = response_html.xpath(r'//form[@name="bigpost"]')

  back_url = response_form[0].attrib['action']
  back_key = response_html.xpath(r'//form//input[@name="wa"][@type="hidden"]')[0].attrib['value']
  back_form = {'wa': back_key}
  #print "Back URL:", back_url
  #print "Back Key:", back_key

  back_response = s.post(back_url, data=back_form)
  #print back_response.text
  back_response_html = lxml.html.fromstring(back_response.text)
  back_response_url = back_response_html.xpath(r'//form[@method="post"]')[0].attrib['action']
  back_response_hidden_elements = back_response_html.xpath(r'//form[@method="post"]//input[@type="hidden"]')
  back_response_form = {x.attrib['name']: x.attrib['value'] for x in back_response_hidden_elements}

  back_response2 = s.post(back_response_url, data=back_response_form)

  r2 = s.get(url)
  #print "Page load URL:", r2.url, "\n"
  #print r2.text

  return r2.text

def other(url):
  s = requests.session()

  page = s.get(url)

  return page.text


# MAIN

with open('data.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    if row[1] == "cms":
      print row[0] + u"|~|" + cms(row[2], row[3], row[4])
    elif row[1] == "blackboard":
      print row[0] + u"|~|" + blackboard(row[2], row[3], row[4])
    elif row[1] == "other":
      print row[0] + u"|~|" + other(row[2])
    elif row[1] == "pdf":
      print row[1]
    else:
      print "NOOO", row[1]

#print cms('https://cmsx.cs.cornell.edu/web/auth/?action=assignment&assignid=529', 'mby8', 'Erdemli72ke4').text
#print blackboard('https://blackboard.cornell.edu/webapps/blackboard/content/listContent.jsp?course_id=_73899_1&content_id=_3368806_1&mode=reset', 'mby8', 'Erdemli72ke4').text
#print blackboard('https://blackboard.cornell.edu/bbcswebdav/pid-3368847-dt-content-rid-10102760_1/xid-10102760_1', 'mby8', 'Erdemli72ke4').text