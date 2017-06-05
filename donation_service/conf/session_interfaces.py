try:
    import cPickle as pickle
except ImportError:
    import pickle
from datetime import datetime, timedelta
import uuid
from uuid import uuid4

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session as DjangoSession
from django.db import close_old_connections
from flask.sessions import SessionInterface, SecureCookieSession
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from lastmiledelivery.clients.user_service_client import get_active_user


class DBInterface(SessionInterface):
    pickle_based = True
    session_class = SecureCookieSession

    def open_session(self, app, request):
        key = request.cookies.get(app.session_cookie_name,
                                  request.headers.get(app.auth_header_name))
        session = None
        try:
            session_obj = DjangoSession.objects.get(
                session_key=key,
                expire_date__gte=datetime.now()
            )
            dump = str(session_obj.session_data)
            session = self.session_class(pickle.loads(dump))
            if session.get('user_id'):
                user = User.objects.get(id=session['user_id'])
                if user.password != session.get('password_hash'):
                    session = None
                    session_obj.delete()
        except DjangoSession.DoesNotExist:
            pass

        if not session:
            session = self.session_class()
            session['key'] = key = str(uuid.uuid4())

        return session

    def save_session(self, app, session, response):
        try:
            domain = self.get_cookie_domain(app)
            path = self.get_cookie_path(app)
            httponly = self.get_cookie_httponly(app)
            secure = self.get_cookie_secure(app)
            expires = self.get_expiration_time(app, session)

            response.set_cookie(app.session_cookie_name, session['key'],
                                expires=expires, httponly=httponly,
                                domain=domain, path=path, secure=secure)
            # response.headers.add_header(app.auth_header_name, key)

            try:
                obj = DjangoSession.objects.get(session_key=session['key'])
            except DjangoSession.DoesNotExist:
                obj = DjangoSession(session_key=session['key'])

            obj.session_data = pickle.dumps(dict(session))
            obj.expire_date = expires or (datetime.now() + timedelta(days=30))
            obj.save()
        finally:
            close_old_connections()


class UserServiceSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, user_id=None, username=None, groups=None,
                 last_login=None):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.user_id = user_id
        self.username = username
        self.groups = groups
        self.last_login = last_login
        self.modified = False


#
class UserServiceInterface(SessionInterface):
    #     pickle_based = False
    session_class = UserServiceSession

    def open_session(self, app, request):
        # print "i am in open session"
        key = request.cookies.get(app.session_cookie_name,
                                  request.headers.get(app.auth_header_name))

        print key
        print '<===============================>'
        facility = request.headers.get(app.facility_header_name, "GJ01")
        session = None
        response_data = get_active_user(token=key, app=app)
        print "===." , response_data
        if not response_data:
            app.logger.info("fatal no session info from user donation_service")
            session = self.session_class()
            session['key'] = key = str(uuid.uuid4())
            session['facility'] = facility
        else:
            print response_data
            response_data["key"] = key
            session = self.session_class(response_data)
            session["key"] = key
            session["username"] = session["guid"]
            session['facility'] = facility

            session["language"] = " "
            session["state"] = " "

            if facility == "MH01":
                session["language"] = "Marathi"
                session["state"] = "Maharashtra"
            elif facility == "GJ01":
                session["language"] = "Gujarati"
                session["state"] = "Gujarat"
            elif facility == "RJ01":
                session["language"] = "Hindi"
                session["state"] = "Rajasthan"
        # print "Done with session"
        return session

    #         session = None
    #         try:
    #             session_obj = DjangoSession.objects.get(
    #                 session_key=key,
    #                 expire_date__gte=datetime.now()
    #             )
    #             dump = str(session_obj.session_data)
    #             session = self.session_class(pickle.loads(dump))
    #             if session.get('user_id'):
    #                 user = User.objects.get(id=session['user_id'])
    #                 if user.password != session.get('password_hash'):
    #                     session = None
    #                     session_obj.delete()
    #         except DjangoSession.DoesNotExist:
    #             pass
    #
    #         if not session:
    #             session = self.session_class()
    #             session['key'] = key = str(uuid.uuid4())
    #
    #         return session

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)

        #        response.set_cookie(app.session_cookie_name, session['key'],
        #                            expires=expires, httponly=httponly,
        #                            domain=domain, path=path, secure=secure)
        close_old_connections()

    #         response.set_cookie(app.facility_cookie_name,"GJ01")
    # def save_session(self, app, session, response):
    #     pass


# try:
#             domain = self.get_cookie_domain(app)
#             path = self.get_cookie_path(app)
#             httponly = self.get_cookie_httponly(app)
#             secure = self.get_cookie_secure(app)
#             expires = self.get_expiration_time(app, session)
# 
#             response.set_cookie(app.session_cookie_name, session['key'],
#                                 expires=expires, httponly=httponly,
#                                 domain=domain, path=path, secure=secure)
#             # response.headers.add_header(app.auth_header_name, key)
# 
#             try:
#                 obj = DjangoSession.objects.get(session_key=session['key'])
#             except DjangoSession.DoesNotExist:
#                 obj = DjangoSession(session_key=session['key'])
# 
#             obj.session_data = pickle.dumps(dict(session))
#             obj.expire_date = expires or (datetime.now() + timedelta(days=30))
#             obj.save()
#         finally:
#             close_old_connections()


# class RedisInterface(SessionInterface):

#     pickle_based = True
#     session_class = SecureCookieSession


#     def open_session(self, app, request):
#         r = redis.StrictRedis(host='localhost', port=6379, db=0)
#         key = request.cookies.get(app.session_cookie_name,
#                                   request.headers.get(app.auth_header_name))
#         session = None
#         try:
#             print key
#             session_obj = r.get(key)
#             if session_obj:
#                 dump = str(session_obj)
#                 session = self.session_class(pickle.loads(dump))
#                 if session.get('user_id'):
#                     user = User.objects.get(id=session['user_id'])
#                     if user.password != session.get('password_hash'):
#                         session = None
#                         r.delete(key)
#         except DjangoSession.DoesNotExist:
#             pass

#         if not session:
#             session = self.session_class()
#             session['key'] = key = str(uuid.uuid4())

#         return session

#     def save_session(self, app, session, response):
#         r = redis.StrictRedis(host='localhost', port=6379, db=0)
#         try:
#             domain = self.get_cookie_domain(app)
#             path = self.get_cookie_path(app)
#             httponly = self.get_cookie_httponly(app)
#             secure = self.get_cookie_secure(app)
#             expires = self.get_expiration_time(app, session)

#             response.set_cookie(app.session_cookie_name, session['key'],
#                                 expires=expires, httponly=httponly,
#                                 domain=domain, path=path, secure=secure)
#             # response.headers.add_header(app.auth_header_name, key)

#             obj = r.get(session['key'])
#             if not obj:
#                 r.set(session["key"],pickle.dumps(dict(session)))
#             # obj.session_data = pickle.dumps(dict(session))
#             # obj.expire_date = expires or (datetime.now() + timedelta(days=30))
#             # obj.save()
#         finally:
#             close_old_connections()

class RedisSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = Redis()
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name,
                                  request.headers.get(app.auth_header_name))
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       request.headers.get(
                                           app.auth_header_name),
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)
