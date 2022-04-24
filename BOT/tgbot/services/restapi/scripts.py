# Скрипты Rest.
def return_error(response):
    return {"code": response.status_code, "error": response.json()["error"]}
