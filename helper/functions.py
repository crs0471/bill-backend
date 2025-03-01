from rest_framework.response import Response
def formated_response(message="Successful!", code=200, dict_={}, dev_message=""):
    if code in [500,501,502]:
        status = "error" 
    elif code in [400,404]:
        status = "info"
    else:
        status = "success"
    response = {
        "message" : message,
        "data" : dict_,
        "dev_message" : dev_message,
        "status": status
    }
    return Response(response, status=code)