import urllib
from django.http import HttpResponseRedirect

def redirect_with_params(url,**kwargs):
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)