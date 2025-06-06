import tiktoken
import logging
from flask import jsonify
import json

logging.basicConfig(level=logging.INFO)

def save_chat_to_txt(chat_history, filename="chat_history.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for msg in chat_history:
                f.write(f"{msg['role'].upper()}: {msg['content']}\n\n")
        logging.info("Chat saved to TXT.")
    except Exception as e:
        logging.error(f"Error saving TXT: {e}")


def save_chat_to_json(chat_history, filename="chat_history.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=2)
        logging.info("Chat saved to JSON.")
    except Exception as e:
        logging.error(f"Error saving JSON: {e}")


def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for msg in messages:
        num_tokens += 4  # role + name + content overhead
        for key, value in msg.items():
            num_tokens += len(encoding.encode(value))
    return num_tokens

def trim_messages(messages, max_tokens, model="gpt-3.5-turbo"):
    logging.info(f"Initial token count: {num_tokens_from_messages(messages, model)}")
    while num_tokens_from_messages(messages, model) > max_tokens:
        if len(messages) > 1:
            removed_msg = messages.pop(1)
            logging.info(f"Trimming message: {removed_msg}")
        else:
            break
    logging.info(f"Final token count: {num_tokens_from_messages(messages, model)}")
    return messages


def safe_response(message):
    logging.error(f'an error happend : {message}')
    return jsonify({"error": message}), 500
