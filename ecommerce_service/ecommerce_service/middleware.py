import json
import logging

access_logger = logging.getLogger('access')

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
        except Exception as e:
            req_body = {str(e)}

        response = self.get_response(request)
        
        log_data = {
            "request_path": request.path,
            "request_body": req_body,
            "response_body": response.content.decode('utf-8') if hasattr(response, 'content') else None,
            "status_code": response.status_code,
        }
        
        access_logger.info(log_data)
        
        return response
