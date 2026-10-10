"""
Module de posting simple et programmé
Usage:
  python -m automat.post --text "Mon message"
  python -m automat.post --text "Avec image" --image chemin/vers/image.jpg
"""

import argparse
from pathlib import Path
from automat.client import get_client
from rich.console import Console

console = Console()


def post_text(text: str, image_path: str | None = None):
    client = get_client()

    if image_path:
        path = Path(image_path)
        if not path.exists():
            console.print(f"[red]Image introuvable : {image_path}[/red]")
            return

        with open(path, "rb") as f:
            img_data = f.read()

        upload = client.upload_blob(img_data)
        embed = {
            "$type": "app.bsky.embed.images",
            "images": [{
                "alt": text[:100] or "Image",
                "image": upload.blob
            }]
        }
        response = client.send_post(text=text, embed=embed)
    else:
        response = client.send_post(text=text)

    console.print(f"[green]✅ Post publié : {response.uri}[/green]")
    return response


def main():
    parser = argparse.ArgumentParser(description="Poster sur Bluesky")
    parser.add_argument("--text", required=True, help="Texte du post")
    parser.add_argument("--image", help="Chemin vers une image (optionnel)")
    args = parser.parse_args()

    post_text(args.text, args.image)


if __name__ == "__main__":
    main()
