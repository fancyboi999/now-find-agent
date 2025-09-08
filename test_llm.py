from langchain_core import messages
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    client = ChatOpenAI(api_key="sk-ct5qFCReZ4vsHYst5c7841D09dD84eCeA23bBfBeE5787413", base_url="https://one-api.nowcoder.com",model="gpt-4o")
    print(client.invoke(input=[{"role": "user", "content": "Hello, how are you?"}]))           