import json

from openai import OpenAI

from app.config import settings


client = OpenAI(api_key=settings.openai_api_key)


def generate_structured_json(
    *,
    system_prompt: str,
    user_prompt: str,
    schema_name: str,
    json_schema: dict,
) -> dict:
    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "schema": json_schema,
                "strict": True,
            }
        },
    )

    return json.loads(response.output_text)