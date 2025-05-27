from time import sleep

from Exceptions import *
from AbstractCommand import AbstractCommand
from APIHandler import APIHandler
from CommandConfig import *


class GetFriendListCommand(AbstractCommand):
    def __init__(self):
        self.__id = None
        self.name = GetFriendList.name
        self.description = GetFriendList.description
        self.__api_handler = APIHandler()

    def run(self, args):
        self.__id = args.id
        user_id = self.__api_handler.get_user_id(self.__id)
        self.display_friend_list(user_id)

    def __get_friends_ids(self, user_id):
        users = self.__api_handler.make_request("friends.get", f"user_id={user_id}")
        if "error" in users:
            error_msg = users["error"]["error_msg"]
            raise PrivateAccountException(error_msg)
        return users["response"]["items"]

    def display_friend_list(self, user_id):
        friends_ids = self.__get_friends_ids(user_id)
        if not friends_ids:
            raise NoFriendsException(f"User {user_id} has no friends :(")
        f_name, l_name = self.__api_handler.get_user_full_name(user_id)
        print(f"\n\033[94mFriend list of {f_name} {l_name}\033[0m")
        for friend in friends_ids:
            sleep(0.1)
            first_name, last_name = self.__api_handler.get_user_full_name(friend)
            print(first_name, last_name)
        else:
            print()
