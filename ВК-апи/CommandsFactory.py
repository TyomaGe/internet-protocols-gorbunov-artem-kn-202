from GetFriendListCommand import GetFriendListCommand
from GetAlbumListCommand import GetAlbumListCommand


class CommandsFactory:
    def get_commands(self):
        return (
            GetFriendListCommand,
            GetAlbumListCommand,
        )
