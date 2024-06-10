import json
import base64
import logging
import mimetypes
from hashlib import sha1
from pathlib import Path
from openai import OpenAI
from typing import Optional, Any
from functools import lru_cache

from zavod import settings
from zavod.logs import get_logger
from zavod.context import Context

log = get_logger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    """Get the OpenAI client."""
    if settings.OPENAI_API_KEY is None:
        raise ValueError("No $OPENSANCTIONS_OPENAI_API_KEY key provided.")
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def encode_file(file: Path, mime_type: Optional[str] = None) -> str:
    """Encode a file as a base64 data URL."""
    if mime_type is None:
        mime_type, _ = mimetypes.guess_type(file.name)
    with open(file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"


def run_image_prompt(
    context: Context,
    prompt: str,
    image_path: Path,
    max_tokens: int = 3000,
    cache_days: int = 60,
    model: str = "gpt-4o",
) -> Any:
    """Run an image prompt."""
    client = get_client()
    image_url = encode_file(image_path)
    cache_hash = sha1(image_url.encode("utf-8"))
    cache_hash.update(prompt.encode("utf-8"))
    cache_key = cache_hash.hexdigest()
    cached_data = context.cache.get_json(cache_key, max_age=cache_days)
    if cached_data is not None:
        log.info("GPT cache hit: %s" % image_path.name)
        return cached_data
    log.info("Prompting %r for: %s" % (model, image_path.name))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=max_tokens,
    )
    assert len(response.choices) > 0
    assert response.choices[0].message is not None
    assert response.choices[0].message.content is not None
    data = json.loads(response.choices[0].message.content)
    context.cache.set_json(cache_key, data)
    return data
