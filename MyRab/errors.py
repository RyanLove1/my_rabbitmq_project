from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = response.status_code
        response.data['msg'] = response.data.get('detail')
        #response.data['data'] = None #可以存在
        if response.data.get('detail'):
            del response.data['detail'] #删除detail字段

    return response



