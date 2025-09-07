from openai import OpenAI


if __name__ == "__main__":
    client = OpenAI(api_key="sk-ct5qFCReZ4vsHYst5c7841D09dD84eCeA23bBfBeE5787413", base_url="https://one-api.nowcoder.com")
    print(client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": "Hello, how are you?"}]))           