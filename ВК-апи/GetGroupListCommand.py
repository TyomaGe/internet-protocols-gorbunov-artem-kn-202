from AbstractCommand import AbstractCommand
from CommandConfig import GetGroupList
from APIHandler import APIHandler
from Exceptions import NoGroupsException, PrivateAccountException


class GetGroupListCommand(AbstractCommand):
    def __init__(self):
        self.__id = None
        self.name = GetGroupList.name
        self.description = GetGroupList.description
        self.__api_handler = APIHandler()

    def run(self, args):
        self.__id = args.id
        user_id = self.__api_handler.get_user_id(self.__id)
        self.display_groups(user_id)

    def __get_groups(self, user_id):
        response = self.__api_handler.make_request(f"groups.get", f"user_id={user_id}&extended=1")
        return response

    def display_groups(self, user_id):
        response = self.__get_groups(user_id)
        if "error" in response:
            error_msg = response["error"]["error_msg"]
            raise PrivateAccountException(error_msg)
        quantity = response["response"]["count"]
        f_name, l_name = self.__api_handler.get_user_full_name(user_id)
        if not quantity:
            raise NoGroupsException(f"{f_name} {l_name} has no groups")
        groups_info = response["response"]["items"]
        print(f"\n\n\033[94m{f_name} {l_name} has {quantity} groups\033[0m")
        for group in groups_info:
            print(group["name"])
        else:
            print()
