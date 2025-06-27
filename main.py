from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/balance-image")
def generate_image(username: str, balance: float, ltc: float, usd: float, user_id: int):
    # Load background (or use a blank image)
    img = Image.new("RGB", (600, 300), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", 24)

    # Format text
    text = f"{username.upper()}\nUsd Balance: ${balance:.2f}\n{ltc:.4f} LTC ≈ ${usd:.2f} USD\nUser ID: {user_id}"
    draw.text((40, 50), text, font=font, fill=(255, 255, 255))

    # Save to bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
   
