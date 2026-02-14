from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import random
import time
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI()

# ---------------- FIREBASE SETUP ----------------
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "ejene-d8ff7",
    "private_key_id": "a2ce7b7cf5ae878769eb6fb2308c2f2c5952d023",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCZT/b14ET8+Z93\nler9lyPPNw8yq119Q7Q3SSs/AseMrozsiW+KEqIR3KI7IbMdcUDSDMVP8FnJnb8v\nsc1h4KBfOX/E7KfPyx7bLtXZmlPcE2VMkKEYv8LSkXLmXcXSutMYlpt29V5eWlEG\nAl+AuJewbDRTbZsKF0QjMNNyrkV9kVgddejVlanGSghZkDfn1wq3E9nZio/E1NPO\nU65lKWrMz+ue9ftjH//ZQTC8GanqaelCcTG9SKu2+TY7WAqGj2QHsaQNzTU292Lk\nMevzYgxbPH94fg1Xl1zvkficQ6IsRbPwTbdobBX+9bl0MmNdq0zyTWdkvdRMc3DI\nt/vtUQ2/AgMBAAECggEAK/CGKDwJqbNlZ+G4wstxgO8X1P7WQZOI8BtxYJLMXF6e\nlyBgrmLevl3MxUPIURTnbgwo9Ns+8JDcfa/o3DeD3ybcnrTw95YQluMaeU5I4JdS\nfhopga1cCfuTwcB4dQgEflST5Ak47bPW6vD9LCg7mV25tXuBZuf6KFfTElguJGl1\nE02OTLK4y8jQPLoTm0ZhSVAaE5AD67EBX28Xs4JXBQxGSfqcWKN9DurkzQdj32zq\ni5HjdSA+gJSTyFSvC6394r5CwD7/hNi+X5M+6PRIRU3Brdjuknz8MLPb3DHrte+x\novF777eAtpswI1q/haeZZ/rlxEuIOdchebfWpO+bgQKBgQDJd03PHjbLw0t3H3IG\n6HngANaZEDCHv8Ns5gkvtPRisha0zrsPn7Db3yPr3RlpSTXyJbBzbutVH2PWLOoe\npnKrtS0XwZgLNe/dmNyjDKtG5egdwXK5HdMdgl3+o507lxSM7mGJz5RrSRnwvaB1\nt5+wZeakVRqS6Y8H/ULj1Y0zfwKBgQDCz9OamwVwOG1AO+0mAemtgNWOQqNSx9+L\ngoOrCys5llZwCiEFUKZpYr9aYRcqK8n/XXWJSaqipXGGbJoPzCUKMoqUQBS6vHTh\nKlP7viaAau4X/FPYVESgf8B8wfxVxCA+gmscHxlhtcquxOVh6kIyO017pAQuIvc6\nKD3gbwRFwQKBgCpqieE/dT31QiA0aKd3rqEwy/2x4OXTw+tbizeWG5Xj9M/gbpXd\ngzjnhAKWrFD0bv0qXjoPclCbqUNgdXI6jQ4FuRa1VbOWiYfYNSvG8RCeOv54yhSb\naOVfmzaPb/0p09PQJI0FPTRRUbrT0cK3BFH5QlP67vtbXRfLhJe/UFk1AoGBAITz\n/29Zcym2aOFYxK2Wypst/RFc60gYvrjgtump8rMXpiBK2WReOWRdD0koT/3o6rAM\nYaXzj6/3B3Z9cdtsMK839RnebgdPjNkK4UxC5tXnpFzcSYCvajK7XWwHnCYQdw0S\nRvVnSBRGVHBYUlAz5z+O9391XaD7Hg0j367nNVxBAoGBAMFIOR5c+0UWHoobxKXX\nuCGxzIpZOjfhrLogE7+7a9jj8PNI4NqPHfs4G7MCRKFv+Garknv/26woBep1Oejy\nPD4bjV5hHUnBS9cXAdvKp874Kzm/qGPRyVdhzM0WlWGosJcf9piF6iOvlOtE8pAX\nDrKyCdpdVa35qdREjA8Th5A+\n-----END PRIVATE KEY-----\n".replace("\\n", "\n"),
    "client_email": "firebase-adminsdk-fbsvc@ejene-d8ff7.iam.gserviceaccount.com",
    "client_id": "101320601096418971113",
    "token_uri": "https://oauth2.googleapis.com/token"
})

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------- ROOT ERROR ----------------
@app.get("/")
async def root():
    return JSONResponse({"error": "error not found"})

# ---------------- LIKE API ----------------
@app.get("/like")
async def like_api(uid: str = None, region: str = None, n: int = None, key: str = None):

    # Check parameters
    if not uid or not region or not n or not key:
        return JSONResponse({"error": "please add your perameter"})

    if key != "444Czy":
        return JSONResponse({"error": "Invalid Key"})

    if n > 200:
        return JSONResponse({"error": "Max 200 allowed per day"})

    doc_ref = db.collection("likes").document(uid)
    doc = doc_ref.get()

    now = int(time.time())
    day_seconds = 86400

    if doc.exists:
        data = doc.to_dict()
        total_today = data.get("total_today", 0)
        last_claim = data.get("last_claim", 0)
        stored_likes = data.get("fake_likes", 0)

        # Reset after 24 hours
        if now - last_claim > day_seconds:
            total_today = 0
    else:
        total_today = 0
        stored_likes = 0

    if total_today + n > 200:
        return JSONResponse({"error": "Your Like Limit Succedd"})

    # Fetch player data
    try:
        response = requests.get(f"https://info-canze1.vercel.app/player-info?uid={uid}")
        player = response.json()["basicInfo"]
    except:
        return JSONResponse({"error": "Player not found"})

    base_liked = player["liked"]

    # Fake increase random (rare case below 200)
    bot_like_value = 200
    if random.randint(1, 20) == 1:
        bot_like_value = random.randint(180, 199)

    # Increase likes
    increase = random.randint(n, n + 20)
    new_total_likes = base_liked + stored_likes + increase

    # Save to Firebase
    doc_ref.set({
        "total_today": total_today + n,
        "last_claim": now,
        "fake_likes": stored_likes + increase
    })

    return JSONResponse({
        "accountId": player["accountId"],
        "nickname": player["nickname"],
        "region": player["region"],
        "level": player["level"],
        "releaseVersion": player["releaseVersion"],
        "liked": new_total_likes,
        "Given Bot": bot_like_value
    })