import openai, dotenv, os

from chat import ChatGPT
dotenv.load_dotenv()
def main():
    chatgpt = ChatGPT(model="text-davinci-003")
    prompt = "Your message: "
    while True:
        input_str = input(prompt)
        response = chatgpt.chat(input_str)
        chatgpt.add_content(input_str, "user")
        chatgpt.add_content(response, "assistant")
        print("GPT-3:", response)
        chatgpt.save_history("history.json")

if __name__ == "__main__":
    print("Welcome to GPT-3 chat!")
    main()