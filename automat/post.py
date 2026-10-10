"""Poster un message sur Bluesky
Usage: python -m automat.post --text "Mon message"
"""
import argparse
from pathlib import Path
from automat.client import get_client

def post_text(text: str, image_path: str | None = None):
    client = get_client()
    if image_path:
        path = Path(image_path)
        if not path.exists():
            raise SystemExit(f"Image introuvable: {image_path}")
        with open(path, "rb") as f:
            img_data = f.read()
        upload = client.upload_blob(img_data)
        embed = {
            "$type": "app.bsky.embed.images",
            "images": [{"alt": (text[:100] or "Image"), "image": upload.blob}],
        }
        response = client.send_post(text=text, embed=embed)
    else:
        response = client.send_post(text=text)
    print(f"Post publié: {response.uri}")
    return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--image", default=None)
    args = parser.parse_args()
    post_text(args.text, args.image)

if __name__ == "__main__":
    main()
