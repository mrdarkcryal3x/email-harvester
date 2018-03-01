#!/usr/bin/python

import sys
import optparse
import urlparse

try:
    from banner import Banner
    from colors import Colors
    from bs4 import BeautifulSoup
    import re
    import requests
    import requests.exceptions
    from collections import deque

except ImportError:
    print 'Install all required libraries'
    sys.exit(1)

colors = Colors()
RED = colors.red()
GREEN = colors.green()
BLUE = colors.blue()
RESET = colors.reset()

class EmailHarvester:

    def __init__(self,urls):
        self.urls = urls
        self.completed_urls = set()
        self.scrapped_emails = set()
        self.tmp_emails = set()

    def scrape_emails(self):
        try:
            while len(self.urls):
                url = self.urls.popleft()
                self.completed_urls.add(url)

                parts = urlparse.urlsplit(url)
                base_url = "{0.scheme}://{0.netloc}".format(parts)
                path = url[:url.rfind('/') + 1] if '/' in parts.path else url

                print GREEN + '[*] Scraping %s ' %url + RESET

                try:
                    response = requests.get(url)
                except requests.exceptions.ConnectionError:
                    print RED + 'Error with url request' + RESET
                    continue

                new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I)) 
                self.scrapped_emails.update(new_emails)
                self.tmp_emails.update(new_emails)
                for email in self.tmp_emails:
                    if '.png' not in email:
                        print BLUE + '[+] %s ' %email + RESET
                self.tmp_emails = set()

                soup = BeautifulSoup(response.text, 'lxml')
            
                for link in soup.find_all('a'):
                    external_link = link.attrs['href'] if "href" in link.attrs else ''
               
                    if external_link.startswith('/'):
                        external_link = base_url + external_link
                    elif not external_link.startswith('http'):
                        external_link = path + external_link
 
                    if not external_link in self.urls and not external_link in self.completed_urls:
                        self.urls.append(external_link)

        except KeyboardInterrupt:
            print RED + '[-] You pressed CTRL+C ' + RESET
    
    
    def print_emails(self):
        for url in self.completed_urls:
            print BLUE + '[+] Completed %s ' %url + RESET
        
        print GREEN + '[!] Found %s emails ' %str(len(self.scrapped_emails)) + RESET

        for email in self.scrapped_emails:
            if '.png' not in email:
                print BLUE + '[+] %s' %email + RESET

    
    def save_to_file(self, path):
        with open(path,'a+') as to_save:
            for email in self.scrapped_emails:
                if '.png' not in email:
                    to_save.write(email+'\n')



def main():

    banner = Banner()

    parser = optparse.OptionParser("Usage python email-gathering.py -u <target url> -f <file to save>")
    parser.add_option('-u', '--url', dest='target_url', type='string', help='Insert target url')
    parser.add_option('-f', '--file', dest='file_path', type='string', help='Insert destination file')
    (options,args) = parser.parse_args()

    target_url = options.target_url
    file_path = options.file_path

    if target_url == None:
        print parser.usage
        sys.exit(1)

    target_url = deque([target_url])



    email_gathering = EmailHarvester(target_url)
    email_gathering.scrape_emails()
    email_gathering.print_emails()

    if file_path != None:
        email_gathering.save_to_file(file_path)


if __name__ == '__main__':
    main()
