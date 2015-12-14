'''
Created on Jun 17, 2010

@author: maksud
'''

from django.http import HttpResponseRedirect
import re
import os

from settings import *

mobile_url = 'http://localhost:8001/'
agents_list = [
    'Nokia', 'bMOT', '^LGE?b', 'SonyEricsson',
    'Ericsson', 'BlackBerry', 'DoCoMo', 'Symbian',
    'Windows CE', 'NetFront', 'Klondike', 'PalmOS',
    'PalmSource', 'portalmm', 'S[CG]H-', 'bSAGEM',
    'SEC-', 'jBrowser-WAP', 'Mitsu', 'Panasonic-',
    'SAMSUNG-', 'Samsung-', 'Sendo', 'SHARP-',
    'Vodaphone', 'BenQ', 'iPAQ', 'AvantGo',
    'Go.Web', 'Sanyo-', 'AUDIOVOX', 'PG-',
    'CDM[-d]', '^KDDI-', '^SIE-', 'TSM[-d]',
    '^KWC-', 'WAP', '^KGT [NC]', 'iPhone',
]
def is_mobile(user_agent):
    for agent in agents_list:
        if re.search(agent, user_agent):
            return True
    return False

#class MobileRedirect(object):
#    def process_request(self, request):
#        if is_mobile(request.META['HTTP_USER_AGENT']):
#            return HttpResponseRedirect(mobile_url)
#        else:
#            pass
#        return None

class MobileRedirect(object):
    def process_request(self, request):
        
        
        
#        if not request.session.get('checked_ua', False):
            
#            print 'OS';
            if is_mobile(request.META['HTTP_USER_AGENT']):
                request.session['checked_ua'] = True
                
                ROOT_PATH = os.path.dirname(__file__)
                TEMPLATE_DIRS = (os.path.join(ROOT_PATH, 'templates/touch'))
#                return HttpResponseRedirect(mobile_url)
            else:
                # Make sure it doesn't try this again
                request.session['checked_ua'] = True
#                TEMPLATE_DIRS = (os.path.join(ROOT_PATH, 'templates/touch'))
                ROOT_PATH = os.path.dirname(__file__)
                TEMPLATE_DIRS = (os.path.join(ROOT_PATH, '../templates/touch'))
            return None
