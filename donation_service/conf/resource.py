from functools import wraps
from flask import request, session, current_app as app
from flask.ext import restful
from lastmiledelivery.conf.error_object import ErrorObject
from lastmiledelivery.exceptions.vaidation_exception import ValidationException
from lastmiledelivery.exceptions.not_found_exception import NotFoundException
from lastmiledelivery.exceptions.invalid_transition import InvalidTransition
from lastmiledelivery.exceptions.unauthorised_exception import UnauthorisedException
from lastmiledelivery.exceptions.generic_custom_exception import GenericCustomException
import sys, traceback
from datetime import datetime, timedelta


def sanitize_response(response):
    data = None
    status = 200
    headers = {}

    if isinstance(response, tuple) and len(response) is 3:
        (data, status, headers) = response
    else:
        data = response

    return (data, status, headers)


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('Source'):
            source = request.headers.get('Source', 'Web')
        # if not request.headers.get('Content-Type') == 'application/json':
        #     raise Exception
        if source == app.config['APPSOURCE']:
            session['platform'] = 'APP'
        else:
            session['platform'] = 'Web'
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        if session.get('username', False):
            return func(*args, **kwargs)

        app.logger.error("Unauthorized request from %s", request.remote_addr)
        return ErrorObject(errorCode=401, errorMessage='Unauthorized.')
    return wrapper


def format_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data, status, headers = sanitize_response(func(*args, **kwargs))
        message = "Operation Successful"
        is_successful = True
        if isinstance(data, ErrorObject):
            status = data.errorCode
            message = data.errorMessage
            data = {}
            is_successful = False

        # patched = isinstance(data, dict) and (
        #     "message" in data and "responseData" in data
        # )

        # if type(data) == dict:
        #     if 'errorCode' in data.keys():
        #         status = data['errorCode']
        if status == 302:
            return data, status, headers

        # if not patched:
        #     if status / 300:
        #         message = "Operation Failed"
        #         status_value = False
        #     else:
        #         message = "Operation Successful"
        #         status_value = True

        #     if type(data) == dict:
        #         if "errorMessage" in data.keys():
        #             message = data["errorMessage"]
        #             data = {}

        data = {
            "responseData": data,
            "message": message,
            "status": is_successful
        }

        # print data

        return (data, status, headers)

    return wrapper


def cors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data, status, headers = sanitize_response(func(*args, **kwargs))

        cors_allow_headers = ', '.join(app.config.get('CORS_ALLOW_HEADERS', []))
        cors_allow_origins = ', '.join(app.config.get('CORS_ALLOW_ORIGINS', []))
        cors_allow_methods = ', '.join(app.config.get('CORS_ALLOW_METHODS', []))

        headers.update({
            'Access-Control-Allow-Headers': cors_allow_headers,
            'Access-Control-Allow-Origin': cors_allow_origins,
            'Access-Control-Allow-Methods': cors_allow_methods
        })

        return (data, status, headers)

    return wrapper


def handle_validation_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start = datetime.now()
            response = func(*args, **kwargs)
            # here is something to remember me by
            end = datetime.now()
            print "API request took {}".format(end-start)
        except UnauthorisedException as kon_hai_be_tu:
            print traceback.print_exc()
            end = datetime.now()
            print "API request took {}".format(end-start)
            return kon_hai_be_tu.errorObject
        except ValidationException as faltugiri_mat_kar:
            print traceback.print_exc()
            end = datetime.now()
            print "API request took {}".format(end-start)
            return faltugiri_mat_kar.errorObject
        except NotFoundException as ghanta_milega:
            print traceback.print_exc()
            end = datetime.now()
            print "API request took {}".format(end-start)
            return ghanta_milega.errorObject
        except InvalidTransition as bhagg_idharse:
            print traceback.print_exc()
            end = datetime.now()
            print "API request took {}".format(end-start)
            return bhagg_idharse.errorObject
        except GenericCustomException as e:
            print traceback.print_exc()
            end = datetime.now()
            print "API request took {}".format(end-start)
            return e.errorObject
        except Exception as ex:
            print "uncaught exception"
            print ex.message
            print traceback.print_exc()
            end = datetime.now()
            print "API request took {}".format(end-start)
            return ErrorObject(errorMessage="Something went wrong", errorCode=400)
        return response

    return wrapper


def gzip(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data, status, headers = sanitize_response(func(*args, **kwargs))


class BaseResource(restful.Resource):
    method_decorators = [handle_validation_exception, authenticate, format_response]
