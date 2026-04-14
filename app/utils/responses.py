def success_response(data, code=200):
    return {"status": "success", "data": data}, code