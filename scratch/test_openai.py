from openai import OpenAI

api_key = "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"

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a professional fact-checker. Answer strictly REAL or FAKE with confidence."},
        {"role": "user", "content": "virat kohli married with anushka sharma"}
    ],
    max_tokens=60
)

print(response.choices[0].message.content)

