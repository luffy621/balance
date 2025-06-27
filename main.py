from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "✅ Balance Image API: Use /balance-image with query params: username, balance, ltc, usd, user_id"
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
        # Load the custom background
        bg_path = "assets/artistic-blurry-colorful-wallpaper-background_58702-8667.webp"
        if not os.path.exists(bg_path):
            return JSONResponse({"error": "Background image not found."}, status_code=500)

        bg = Image.open(bg_path).convert("RGBA")
        img = bg.copy()

        draw = ImageDraw.Draw(img)

        # Load font — use default if missing
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()

        # Compose text
        lines = [
            f"{username.upper()}",
            f"Usd Balance: ${balance:.2f}",
            f"{ltc:.4f} LTC ≈ ${usd:.2f} USD",
            f"User ID: {user_id}"
        ]

        x, y = 40, 50
        line_spacing = 50

        for line in lines:
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
            y += line_spacing

        # Save and respond with image
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
