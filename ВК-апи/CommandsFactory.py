from GetFriendListCommand import GetFriendListCommand
from GetAlbumListCommand import GetAlbumListCommand
from GetGroupListCommand import GetGroupListCommand


class CommandsFactory:
    def get_commands(self):
        return (
            GetFriendListCommand,
            GetAlbumListCommand,
            GetGroupListCommand
        )
