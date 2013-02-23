from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.template.context import RequestContext
import json
import requests


def login_user(request):
    context = dict()
    context = {
        'REDIRECT_URL': settings.REDIRECT_URL,
        'CLIENT_ID': settings.CLIENT_ID,
    
    }
    return render_to_response('loginpage.html', context)  # Create your views here.

def validateUser(request):
    context = dict()
    code = request.GET.get('code', None)
    print code
    error = request.GET.get('error_description', None)
    if code:
        r = requests.post(settings.INSTAGRAM_OAUTH_ACCESS_TOKEN_URL, data={
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': '{0}instagram/auth/'.format(settings.SITE_ROOT_URI),
            'code': code,
        })

        data = json.loads(r.text)
        error = data.get('error_message', None)

        if not error:
            print 'user successfully verified'
            print data['access_token']
            context['token'] = data['access_token']
            context['user_id'] = data['user'].get('id', None)
            context['user_name'] = data['user'].get('full_name', None)
            request.session['accessToken'] = data['access_token']
            return HttpResponseRedirect(reverse('userPage', args=(data['user'].get('id', None),)))
    

    # return render_to_response('instagram.html', context)  # Create your views here.
    return HttpResponseRedirect(reverse('loginpage',))
    # return redirect('instagram', context)


    # return render_to_response('loginpage.html')# Create your views here.


def instagram(request, userID):
    context = dict()
    if 'accessToken' in request.session:
        user_r = requests.get('{0}users/{1}/?access_token={2}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            request.session['accessToken']))
        user_follows = requests.get('{0}users/{1}/follows?access_token={2}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            request.session['accessToken']))
        user_followedby = requests.get('{0}users/{1}/followed-by?access_token={2}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            request.session['accessToken']))
        user_data = json.loads(user_r.text)
        user_follows_data = json.loads(user_follows.text)
        user_followedby_data = json.loads(user_followedby.text)
        print request.session['accessToken']
     
        media_r = requests.get('{0}users/{1}/media/recent/?access_token={2}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            request.session['accessToken']))
        media_data = json.loads(media_r.text)
        print user_follows_data
        print user_follows_data.get('data',None)
        context = {
            'user': user_data.get('data', None),
            'media': media_data.get('data', None),
            'pagination': media_data.get('pagination', None),
            'follows':len(user_follows_data.get('data')),
            'followedBy':len(user_followedby_data.get('data')),
            'firstPage':True,
        
        }
        return render_to_response('instagram.html', context, context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('loginpage',))

def instagramNext(request, userID, maxId):
    session = SessionStore(session_key=request.session.session_key)
    if 'accessToken' in session:
        accessToken= session['accessToken']
        print accessToken
        context = dict()
        user_r = requests.get('{0}users/{1}/?access_token={2}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            accessToken))
        user_data = json.loads(user_r.text)
        user_follows = requests.get('{0}users/{1}/follows?access_token={2}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            accessToken))
        user_followedby = requests.get('{0}users/{1}/followed-by?access_token={2}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            accessToken))
        user_follows_data = json.loads(user_follows.text)
        user_followedby_data = json.loads(user_followedby.text)
        media_r = requests.get('{0}users/{1}/media/recent/?access_token={2}&max_id={3}'.format(
            settings.INSTAGRAM_API_URL,
            userID,
            accessToken,
            maxId))
        media_data = json.loads(media_r.text)
        context = {
            'user': user_data.get('data', None),
            'media': media_data.get('data', None),
            'pagination': media_data.get('pagination', None),
            'follows':len(user_follows_data.get('data')),
            'followedBy':len(user_followedby_data.get('data')),
            'firstPage':False,
        
        }
        return render_to_response('instagram.html', context, context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('loginpage',))

