from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # Since user_credentials = schemas.UserLogin, you could query with
    # user_credentials.email but now
    # user_credentials = OAuth2PasswordRequestForm so ".email" turns
    # into ".username" (it can be email, username, id, w/e dev sends to it)
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    # If user does not exist,
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # If passwords do not match,
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token,
            "token_type": "bearer"}
