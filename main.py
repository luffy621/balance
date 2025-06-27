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
        # Load background image
        bg_path = "assets/artistic-blurry-colorful-wallpaper-background_58702-8667.webp"
        if not os.path.exists(bg_path):
            return JSONResponse({"error": "Background not found."}, status_code=500)
        bg = Image.open(bg_path).convert("RGBA")
        img = bg.copy()
        draw = ImageDraw.Draw(img, "RGBA")

        # Draw semi-transparent card
        pad = 30
        card = [pad, pad, img.width - pad, img.height - pad]
        draw.rounded_rectangle(
            card,
            radius=20,
            fill=(0, 0, 0, 180),
            outline=(255, 255, 255, 200),
            width=2
        )

        def load_font(path, size):
            try:
                return ImageFont.truetype(path, size)
            except:
                return None

        # Load fonts
        username_size = 48
        detail_size = 32

        username_font = (
            load_font("assets/Inter-Bold.ttf", username_size)
            or load_font("arial.ttf", username_size)
            or ImageFont.load_default()
        )

        detail_font = (
            load_font("assets/Inter-Regular.ttf", detail_size)
            or load_font("arial.ttf", detail_size)
            or ImageFont.load_default()
        )

        # Prepare lines of text
        lines = [
            (username.upper(), username_font, (255, 255, 255, 255)),
            (f"USD Balance: ${balance:.2f}", detail_font, (180, 255, 200, 255)),
            (f"{ltc:.4f} LTC ≈ ${usd:.2f} USD", detail_font, (200, 200, 255, 255)),
            (f"User ID: {user_id}", detail_font, (200, 200, 200, 255)),
        ]

        # Draw text lines
        x, y = pad + 20, pad + 20
        spacing = 10
        for text, font, color in lines:
            draw.text((x, y), text, font=font, fill=color)
            bbox = font.getbbox(text)
            height = bbox[3] - bbox[1]
            y += height + spacing

        # Return image
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
