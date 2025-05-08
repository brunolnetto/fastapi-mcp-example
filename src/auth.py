from fastapi import Depends, HTTPException

def get_current_user(token: str = "fake-token"):
    if token != "fake-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "johndoe"}
