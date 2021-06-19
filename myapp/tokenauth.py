
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async

import urllib.parse
import urllib.parse as urlparse
from urllib import parse

from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status

#Token or User getting must be called outside THREAD with @dataase_sync_to_async
@database_sync_to_async
def get_user(token):
    try:
        print("Token")
        token = Token.objects.get(key=token)
        return token.user
    except Token.DoesNotExist:
        print("Does Not Exist")
        return AnonymousUser()
    except Exception:
        return AnonymousUser()
    
#Custom Token Auth MiddleWare which gets eecuted first.
class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner



    async def __call__(self, receive, send):
        print("92")
        print(self.scope)
        decoded_qs = urllib.parse.parse_qs(self.scope["query_string"])
        print(decoded_qs)
        if b'token' in decoded_qs:
          token = decoded_qs.get(b'token').pop().decode()
          self.scope['user'] = await get_user(token)
        print("else block")
        return await self.inner(self.scope, receive, send)


#TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(inner)  #connects only when token params is present as a queryString
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))  # => AuthMidlewareStack for Session or Cookie Connection
#throws error when u try to login from a cookie or session browser 

 