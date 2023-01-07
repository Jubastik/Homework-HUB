class ApiError:
    def __init__(self, status, json):
        print(json)
        self.error = json
        self.status_code = status
        self.msg = json["detail"][0]["msg"]
        self.error_code = json["ErrorID"]
    
    def handle(self, user):
        pass