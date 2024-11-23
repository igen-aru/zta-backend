from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from datetime import datetime, timedelta

# Configuration
SECRET_KEY = "your_secret_key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize FastAPI app
app = FastAPI()

# Mock User Database
users_db = {
    "user1": {"username": "user1", "password": "password1", "role": "admin"},
    "user2": {"username": "user2", "password": "password2", "role": "viewer"},
}

# CORS Middleware for Frontend Communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://zta-frontend.vercel.app"],  # Replace with your deployed frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper Functions
def authenticate_user(username: str, password: str):
    """Authenticate user credentials."""
    user = users_db.get(username)
    if user and user["password"] == password:
        return user
    return None

def create_access_token(data: dict, expires_delta: timedelta):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Routes
@app.get("/")
def read_root():
    """Root Endpoint."""
    return {"message": "Welcome to the ZTA Backend"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login Endpoint to issue JWT token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
