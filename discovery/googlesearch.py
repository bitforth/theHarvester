import myparser
import re
import time
import http.client


class SearchGoogle:
    def __init__(self, word, limit, offset):
        self.word = word
        self.files = "pdf"
        self.results = ""
        self.totalresults = ""
        self.server = "www.google.com"
        self.server_api = "www.googleapis.com"
        self.hostname = "www.google.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6)"
        self.quantity = "100"
        self.limit = limit
        self.counter = offset
        self.api_key = "AIzaSyBuBomy0n51Gb4836isK2Mp65UZI_DrrwQ"

    def do_search(self):

        h = http.client.HTTPConnection(self.server)
        h.putrequest('GET', "/search?num=" + self.quantity + "&start=" + str(
            self.counter) + "&hl=en&meta=&q=%40\"" + self.word + "\"")
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        res = h.getresponse()
        self.results = str(res.read())
        self.totalresults += self.results

    def do_search_api(self):
        h = http.client.HTTPSConnection(self.server_api)
        h.putrequest('GET', "/customsearch/v1?key=" + self.api_key + "&start=" + str(
            self.counter) + "&q=%40\"" + self.word + "\"")
        h.putheader('Host', self.server_api)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        h.getresponse()
        self.results = h.getfile().read()
        self.totalresults += self.results
        print(self.totalresults)


    def do_search_files(self, files):
        h = http.client.HTTPConnection(self.server)
        h.putrequest('GET', "/search?num=" + self.quantity + "&start=" + str(
            self.counter) + "&hl=en&meta=&q=filetype:" + files + "%20site:" + self.word)
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        self.results = h.getfile().read()
        self.totalresults += self.results

    def do_search_profiles(self):
        h = http.client.HTTPConnection(self.server)
        h.putrequest('GET', '/search?num=' + self.quantity + '&start=' + str(
            self.counter) + '&hl=en&meta=&q=site:www.google.com%20intitle:"Google%20Profile"%20"Companies%20I%27ve%20worked%20for"%20"at%20' + self.word + '"')
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        self.results = h.getfile().read()
        self.totalresults += self.results

    def check_next(self):
        renext = re.compile('>  Next  <')
        nextres = renext.findall(self.results)
        if not [] == nextres:
            nexty = "1"
        else:
            nexty = "0"
        return nexty

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_files(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.fileurls(self.files)

    def get_profiles(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.profiles()

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            # more = self.check_next()
            time.sleep(1)
            print("\tSearching " + str(self.counter) + " results...")
            self.counter += 100

    def process_api(self):
        while self.counter <= self.limit:
            self.do_search_api()
            print("\tSearching " + str(self.counter) + " results...")
            self.counter += 100

    def process_files(self, files):
        while self.counter <= self.limit:
            self.do_search_files(files)
            time.sleep(1)
            self.counter += 100
            print("\tSearching " + str(self.counter) + " results...")

    def process_profiles(self):
        while self.counter < self.limit:
            self.do_search_profiles()
            time.sleep(0.3)
            self.counter += 100
            print("\tSearching " + str(self.counter) + " results...")