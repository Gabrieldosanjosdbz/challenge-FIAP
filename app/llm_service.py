import base64
import io
import requests
#from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv
import json


load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  

# def encode_image_to_base64(image_url: str) -> str:
#     headers = {"User-Agent": "College project demo"}
#     response = requests.get(image_url, headers=headers, timeout=60)
#     response.raise_for_status()
#     img = Image.open(io.BytesIO(response.content))
#     img_format = img.format.lower()
#     base64_image = base64.b64encode(response.content).decode("utf-8")
#     return f"data:image/{img_format};base64,{base64_image}"

async def analisar_painel(url: str) -> dict:
    """
    url: URL de uma única imagem
    temperatura: float de 0.0 a 1.0
    """



    imagem_formatada = {
        "type": "image_url",
        "image_url": {"url": url}
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are an assistant that analyzes solar panel images.
                Verify with the image if the solar panel needs cleaning to make sure the efficiency will be high.
                If it needs cleaning, set 'needCleaning' to true.
                else set it to false.
                Also, measure the insolation in the image and classify it:
                - 3 for high insolation
                - 2 for medium
                - 1 for low
                Set the value in the `nivelSolar` column.
                also make a large analyse of the image  in portuguese and justify your response please we will use your analyse to comunicate with the user of our system with a Text to speech so dont use therms like the first or the second
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