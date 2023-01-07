class ApiError:
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        self.msg = error["detail"]["msg"]
        self.error_code = error["ErrorID"]
    
    def handle(self, user):
        pass