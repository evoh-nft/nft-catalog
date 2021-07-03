#!/bin/python3

import json
from pathlib import Path

import requests

# modify these prior to using the script
PINATA_API: str = ""
PINATA_SECRET: str = ""


def pin_collection(collection: str) -> None:
    """
    Pin an entire collection.
    """
    base_path = Path(__file__).parent.joinpath(f"../collections/{collection}/images").resolve()
    if not base_path.exists():
        raise ValueError("Invalid collection name")
    for path in base_path.glob("*.png"):
        pin_nft(collection, path.stem)


def pin_nft(collection: str, image_id: str) -> None:
    """
    Pin a single NFT from a collection.
    """
    base_path = Path(__file__).parent.joinpath(f"../collections/{collection}").resolve()
    if not base_path.exists():
        raise ValueError("Invalid collection name")
    image_hash = pin_image(base_path.joinpath(f"images/{image_id}.png"))
    metadata_hash = pin_json(base_path.joinpath(f"metadata/{image_id}.json"))
    print(f"\n{collection}/{image_id}\n  Image: {image_hash}\n  Metadata: {metadata_hash}")


def pin_image(path: Path) -> str:
    with path.open("rb") as fp:
        image_binary = fp.read()
    response = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        headers={"pinata_api_key": PINATA_API, "pinata_secret_api_key": PINATA_SECRET},
        files={"file": image_binary},
        timeout=1800,
    ).json()
    return response["IpfsHash"]


def pin_json(path: Path) -> str:
    with path.open("r") as fp:
        data = json.load(fp)
    response = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        headers={"pinata_api_key": PINATA_API, "pinata_secret_api_key": PINATA_SECRET},
        json=data,
    ).json()
    return response["IpfsHash"]
