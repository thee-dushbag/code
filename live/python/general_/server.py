# type: ignore

from time import localtime, time, asctime
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.resource import Resource
from string import Template

html = Template("<h1><center>$key = $val</center></h1>")

class YearPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        return html.substitute(key='year', val=localtime(time()).tm_year).encode()

class SecPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        return html.substitute(key='second', val=localtime(time()).tm_sec).encode()


class HourPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        return html.substitute(key='hour', val=localtime(time()).tm_hour).encode()

class MinPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        return html.substitute(key='min', val=localtime(time()).tm_min).encode()


class TimePage(Resource):
    def getChild(self, path, request):
        if path == b'':
            return self
        return super().getChild(path, request)

    def render_GET(self, request):
        return html.substitute(key='time', val=asctime(localtime(time()))).encode()


class ClockSite(Resource):
    def getChild(self, path, request):
        if path == b'':
            return self
        return super().getChild(path, request)

    def render_GET(self, request):
        return html.substitute(key="path", val="Clock Site").encode()

timepage = TimePage()
timepage.putChild(b'hour', HourPage())
timepage.putChild(b'minute', MinPage())
timepage.putChild(b'second', SecPage())

resrc = ClockSite()
resrc.putChild(b'year', YearPage())
resrc.putChild(b'time', timepage)

site = Site(resrc)
reactor.listenTCP(8000, site)
reactor.run()

