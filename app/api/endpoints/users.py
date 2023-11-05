from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.data_models.user import UserOut
    
router = APIRouter()

@router.get("/users/me/", response_model=UserOut)
def read_users_me(current_user: str = Depends(get_current_user)):
    return current_user

# @router.put("/users/{user_id}", response_model=UserOut)
# def update_user_details(user: )
