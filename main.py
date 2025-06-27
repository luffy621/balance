
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

app = FastAPI()

# --- Configuration ---
# Create an 'assets' directory and place your background and font files there.
BG_PATH = "assets/artistic-blurry-colorful-wallpaper-background_58702-8667.webp"
FONT_BOLD_PATH = "assets/fonts/DejaVuSans-Bold.ttf"  # Example: Bold font for titles
FONT_REGULAR_PATH = "assets/fonts/DejaVuSans.ttf" # Example: Regular font for text

# --- Helper Functions ---
def load_font(path, size):
    """Loads a font file, with a fallback to a default font if not found."""
    try:
        return ImageFont.truetype(path, size)
    except IOError:
        print(f"Warning: Font not found at {path}. Using default font.")
        return ImageFont.load_default()

@app.get("/")
def root():
    """API root endpoint with usage instructions."""
    return {
        "message": "✅ Balance Image API: GET /balance-image?username=...&balance=...&ltc=...&usd=...&user_id=..."
    }

@app.get("/balance-image")
def generate_image(
    username: str = "Anonymous",
    balance: float = 0.0,
    ltc: float = 0.0,
    usd: float = 0.0,
    user_id: int = 0
):
    """Generates and returns a customized image with user balance details."""
    try:
        # 1) Validate that the background image exists
        if not os.path.exists(BG_PATH):
            return JSONResponse({"error": f"Background image not found at {BG_PATH}"}, status_code=500)

        # 2) Load background image
        with Image.open(BG_PATH).convert("RGBA") as bg:
            img = bg.copy()
            draw = ImageDraw.Draw(img, "RGBA")

            # 3) Load fonts with different sizes
            # --- CUSTOMIZE YOUR FONTS AND SIZES HERE ---
            font_title = load_font(FONT_BOLD_PATH, 60)
            font_large = load_font(FONT_REGULAR_PATH, 48)
            font_medium = load_font(FONT_REGULAR_PATH, 32)
            font_small = load_font(FONT_REGULAR_PATH, 24)

            # 4) Define content and positions
            # --- CUSTOMIZE YOUR TEXT LAYOUT HERE ---
            # (x, y) coordinates from the top-left corner.
            y_position = 100  # Initial Y position
            x_padding = 50   # Padding from the left edge

            # Draw "Username"
            draw.text((x_padding, y_position), f"User: {username}", font=font_medium, fill="white")
            y_position += 60 # Move down for the next line

            # Draw "User ID"
            draw.text((x_padding, y_position), f"ID: {user_id}", font=font_small, fill="#E0E0E0")
            y_position += 150 # Add a larger gap

            # Draw "Balance" - using the bold title font
            draw.text((x_padding, y_position), "Total Balance", font=font_medium, fill="white")
            y_position += 50
            draw.text((x_padding, y_position), f"${balance:,.2f}", font=font_title, fill="white")
            y_position += 120

            # Draw LTC and USD values using different font sizes
            draw.text((x_padding, y_position), f"LTC: {ltc}", font=font_large, fill="#DDDDDD")
            y_position += 70
            draw.text((x_padding, y_position), f"USD Value: ${usd:,.2f}", font=font_medium, fill="#DDDDDD")

            # 5) Return image as a PNG stream
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        print(f"An error occurred: {e}") # Log the full error to the console
        return JSONResponse({"error": "An internal server error occurred. Check logs for details."}, status_code=500)
