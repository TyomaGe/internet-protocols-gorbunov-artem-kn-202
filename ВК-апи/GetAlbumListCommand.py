from AbstractCommand import AbstractCommand
from CommandConfig import GetAlbumList
from APIHandler import APIHandler
from Exceptions import NoAlbumsException


class GetAlbumListCommand(AbstractCommand):
    def __init__(self):
        self.__id = None
        self.name = GetAlbumList.name
        self.description = GetAlbumList.description
        self.__api_handler = APIHandler()

    def run(self, args):
        self.__id = args.id
        user_id = self.__api_handler.get_user_id(self.__id)
        self.display_albums(user_id)

    def __get_albums(self, user_id):
        response = self.__api_handler.make_request(f"photos.getAlbums", f"owner_id={user_id}")
        return response

    def display_albums(self, user_id):
        response = self.__get_albums(user_id)
        quantity = response["response"]["count"]
        f_name, l_name = self.__api_handler.get_user_full_name(user_id)
        if not quantity:
            raise NoAlbumsException(f"{f_name} {l_name} has no albums")
        albums_info = response["response"]["items"]
        print(f"\n\n\033[94m{f_name} {l_name} has {quantity} albums\033[0m")
        for album in albums_info:
            album_title = album["title"]
            album_size = album["size"]
            print(f"{album_title} with {album_size} images")
        else:
            print()
