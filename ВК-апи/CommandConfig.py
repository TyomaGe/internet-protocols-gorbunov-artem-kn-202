from dataclasses import dataclass


@dataclass(frozen=True)
class GetFriendList:
    name = "friends"
    description = ""


@dataclass(frozen=True)
class GetAlbumList:
    name = "albums"
    description = ""


@dataclass(frozen=True)
class GetGroupList:
    name = "groups"
    description = ""
