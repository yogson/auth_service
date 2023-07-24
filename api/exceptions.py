from fastapi import HTTPException

bad_creds = HTTPException(status_code=400, detail="Incorrect username or password")