#!/usr/bin/env python

from bs4 import BeautifulSoup as soupy
import requests

def login_elements(tag):
    """A filter to find cas login form elements"""
    return tag.has_key('name') and tag.has_key('value')

def login(username, password, url):
    cas_page = requests.get(url)
    cas_doc = soupy(cas_page.text)
    form_inputs = cas_doc.find_all(login_elements)

    login_data = dict()
    for tag in form_inputs:
        login_data[tag['name']] = tag['value']

    login_data['username'] = username
    login_data['password'] = password

    signin_page = requests.post(url, login_data, cookies=cas_page.cookies)

    if "Log In Successful" in signin_page.text:
        return signin_page.cookies
    else:
        return False

if __name__ == '__main__':
    import argparse
    import getpass

    parser = argparse.ArgumentParser(description='Attempt to log in to CAS.')
    parser.add_argument('-u', dest='username', default=getpass.getuser())
    parser.add_argument('-p', dest='password')
    parser.add_argument('URL', type=str, nargs=1,
                        help="CAS base i.e. https://sso.example.com/cas/login")

    args = parser.parse_args()
    if not args.password:
        prompt = 'Password for "{0.username}" on {0.URL[0]}: '.format(args) 
        args.password = getpass.getpass(prompt)
    print login(args.username, args.password, args.URL[0])
