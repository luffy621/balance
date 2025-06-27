from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Welcome to the Balance Image API 🪙 — Use /balance-image with query params: username, balance, ltc, usd, user_id"
    }

@app.get("/balance-image")
def generate_image(username: str, balance: float, ltc: float, usd: float, user_id: int):
    try:
        # Create a blank image (dark background)
        img = Image.new("RGB", (600, 300), color=(24, 24, 24))
        draw = ImageDraw.Draw(img)

        # Try to load truetype font, fall back if fails
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        # Compose the text
        text = (
            f"{username.upper()}\n"
            f"Usd Balance: ${balance:.2f}\n"
            f"{ltc:.4f} LTC ≈ ${usd:.2f} USD\n"
            f"User ID: {user_id}"
        )

        draw.text((40, 60), text, font=font, fill=(255, 255, 255))

        # Convert to byte stream
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}

