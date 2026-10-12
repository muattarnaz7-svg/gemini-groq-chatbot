import sys

from google.genai import errors

import chat_store
from assistant import SYSTEM_PROMPT, create_client, stream_reply


def main() -> int:
    try:
        client = create_client()
    except RuntimeError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    chat_id = chat_store.new_chat_id()
    history: list[dict[str, str]] = []
    print("Chatbot ready! Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        request_messages = [*history, {"role": "user", "content": user_input}]
        print("Bot: ", end="", flush=True)
        reply = ""
        try:
            for text in stream_reply(client, request_messages, SYSTEM_PROMPT):
                print(text, end="", flush=True)
                reply += text
        except errors.APIError as exc:
            print(f"\nGemini API request failed: {exc}\n")
            continue

        print("\n")
        history.extend(
            [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": reply},
            ]
        )
        chat_store.save_chat(chat_id, history)  # same saved chats as the web app

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
