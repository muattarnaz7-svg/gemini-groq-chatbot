import sys

import chat_store
from assistant import (
    API_ERRORS,
    PROVIDERS,
    SYSTEM_PROMPT,
    create_client,
    stream_reply,
)


def choose_provider() -> str:
    print("Kon sa model use karna hai?")
    for i, name in enumerate(PROVIDERS, 1):
        print(f"  {i}. {name}")

    while True:
        try:
            choice = input("Number likhein: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            raise SystemExit(0)

        if choice.isdigit() and 1 <= int(choice) <= len(PROVIDERS):
            return PROVIDERS[int(choice) - 1]
        print(f"Galat choice. 1 se {len(PROVIDERS)} ke beech number likhein.")


def main() -> int:
    provider = choose_provider()

    try:
        client = create_client(provider)
    except RuntimeError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    chat_id = chat_store.new_chat_id()
    history: list[dict[str, str]] = []
    print(f"\n{provider} chatbot ready! Type 'quit' or 'exit' to stop.\n")

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
            for text in stream_reply(client, request_messages, SYSTEM_PROMPT, provider):
                print(text, end="", flush=True)
                reply += text
        except API_ERRORS as exc:
            print(f"\n{provider} API request failed: {exc}\n")
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