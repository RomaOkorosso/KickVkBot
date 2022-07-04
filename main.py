from typing import List
import argparse
import vk_api
import dotenv


def parse_chat_id(example) -> int:
    chat_id = ""
    if "sel=" in example:
        chat_id = example[example.find("sel=") + len("sel=") :]
        if "c" in chat_id:
            chat_id = chat_id.replace("c", "")

    chat_id = int(chat_id)
    return chat_id


def first_run():
    config = dotenv.dotenv_values(".env")

    login = config.get("login")
    password = config.get("password")

    session = vk_api.VkApi(login, password)
    session.auth()


def kick_non_admin_users(chat_id) -> None:
    config = dotenv.dotenv_values(".env")

    login = config.get("login")
    password = config.get("password")

    session = vk_api.VkApi(login, password)
    session.auth(token_only=True)
    vk = session.get_api()

    u = vk.messages.getConversationMembers(peer_id=2000000000 + chat_id)

    u_items: List[dict] = u["items"]
    success, errors = 0, 0

    for item in u_items:
        if not item.get("is_admin", None):
            res = vk.messages.removeChatUser(
                chat_id=chat_id, member_id=item["member_id"]
            )
            if res == 1:
                success += 1
            else:
                errors += 1

    print(f"End with {success} with success\n{errors} with errors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="kick non admin users")
    parser.add_argument("-L", "--link", help="link to chat", action="store_true")
    parser.add_argument(
        "-O",
        "--first_run",
        help="needs to run at first time",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()
    print(args.first_run)
    if args.first_run:
        first_run()
        exit(0)
    chat_id = parse_chat_id(args.link)
    kick_non_admin_users(chat_id)
