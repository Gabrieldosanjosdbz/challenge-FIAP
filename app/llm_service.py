import base64
import io
import requests
from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  

def encode_image_to_base64(image_url: str) -> str:
    headers = {"User-Agent": "College project demo"}
    response = requests.get(image_url, headers=headers, timeout=60)
    response.raise_for_status()
    img = Image.open(io.BytesIO(response.content))
    img_format = img.format.lower()
    base64_image = base64.b64encode(response.content).decode("utf-8")
    return f"data:image/{img_format};base64,{base64_image}"

async def analisar_painel(url: str) -> dict:
    """
    url: URL de uma única imagem
    temperatura: float de 0.0 a 1.0
    """

    base64_url = encode_image_to_base64(url)

    imagem_formatada = {
        "type": "image_url",
        "image_url": {"url": base64_url}
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are an assistant that analyzes a solar panel image.
                Verify if the solar panel needs cleaning and measure insolation.

                Output format: JSON with fields
                {
                    "id": 1,
                    "needCleaning": <true/false>,
                    "nivelSolar": <1|2|3>,
                    "analise": "<string>"
                }
                """
            },
            {
                "role": "user",
                "content": [imagem_formatada]
            }
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    # Se content for string, transforma em dict
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            raise Exception(f"Não foi possível converter a resposta da LLM em JSON: {content}")

    return content