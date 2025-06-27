from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "✅ Balance Image API: GET /balance-image?username=...&balance=...&ltc=...&usd=...&user_id=..."
    }

@app.get("/balance-image")
def generate_image(
    username: str,
    balance: float,
    ltc: float,
    usd: float,
    user_id: int
):
    try:
        # 1) Load background
        bg_path = "assets/background.png"
        if not os.path.exists(bg_path):
            return JSONResponse({"error": "Background not found."}, status_code=500)
        bg = Image.open(bg_path).convert("RGBA")
        img = bg.copy()
        draw = ImageDraw.Draw(img, "RGBA")

        # 2) Overlay is just the raw background—no card this time

        # 3) Load your exact fonts & sizes
        def load_font(path, size):
            try:
                return ImageFont.truetype(path, size)
            except:
                return None

        # these sizes match your screenshot
        USERNAME_SIZE = 36
        DETAILS_SIZE  = 28

        username_font = (
            load_font("assets/YourFont-Bold.ttf", USERNAME_SIZE)
            or ImageFont.load_default()
        )
        detail_font = (
            load_font("assets/YourFont-Regular.ttf", DETAILS_SIZE)
            or ImageFont.load_default()
        )

        # 4) Prepare the lines exactly as in your file
        lines = [
            (username.upper(), username_font),
            (f"Usd Balance: {balance}", detail_font),
            (f"{ltc} LTC ≈ ${usd} USD", detail_font),
            (f"User ID: {user_id}", detail_font),
        ]

        # 5) Starting position & exact spacing
        x, y = 40, 40
        for text, font in lines:
            # draw in white
            draw.text((x, y), text, font=font, fill=(255,255,255,255))
            # compute height of this line
            bbox = font.getbbox(text)
            height = bbox[3] - bbox[1]
            # add an extra blank line between entries (same height)
            y += height * 2

        # 6) Return PNG
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
