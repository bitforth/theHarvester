import http.client
import myparser


class SearchGoogleLabs:
    def __init__(self, arguments):
        self.results = ""
        self.totalresults = ""
        self.server = "labs.google.com"
        self.hostname = "labs.google.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        i = 0
        self.set = ""
        for argument in arguments:
            i += 1
            if i == 1:
                self.set = self.set + "q" + str(i) + "=" + str(argument)
            else:
                self.set = self.set + "&q" + str(i) + "=" + str(argument)

    def do_search(self):
        h = http.client.HTTPConnection(self.server)
        h.putrequest('GET', "/sets?hl=en&" + self.set)
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        h.getreply()
        self.results = h.getfile().read()
        self.totalresults += self.results

    def get_set(self):
        rawres = myparser.parser(self.totalresults, list)
        return rawres.set()

    def process(self):
        self.do_search()