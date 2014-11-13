import http.client
import myparser


class SearchPGP:
    def __init__(self, word):
        self.word = word
        self.results = ""
        self.server = "pgp.rediris.es:11371"
        self.hostname = "pgp.rediris.es"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"

    def process(self):
        h = http.client.HTTPSConnection(self.server)
        h.putrequest('GET', "/pks/lookup?search=" + self.word + "&op=index")
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        self.results = h.getfile().read()


    def get_emails(self):
        rawres = myparser.parser(self.results, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.results, self.word)
        return rawres.hostnames()