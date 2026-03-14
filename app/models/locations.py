
from .common import ApiModel, BadgeUrls, ClanReference, ItemsResponse, League, Location


class LocationListResponse(ItemsResponse[Location]):
    pass


class ClanRanking(ApiModel):
    tag: str
    name: str
    location: Location
    badgeUrls: BadgeUrls | None = None
    clanLevel: int
    members: int
    clanPoints: int
    rank: int
    previousRank: int


class ClanRankingListResponse(ItemsResponse[ClanRanking]):
    pass


class ClanBuilderBaseRanking(ApiModel):
    tag: str
    name: str
    location: Location
    badgeUrls: BadgeUrls | None = None
    clanLevel: int
    members: int
    clanBuilderBasePoints: int
    clanPoints: int | None = None
    rank: int
    previousRank: int


class ClanBuilderBaseRankingListResponse(ItemsResponse[ClanBuilderBaseRanking]):
    pass


class ClanCapitalRanking(ApiModel):
    tag: str
    name: str
    location: Location
    badgeUrls: BadgeUrls | None = None
    clanLevel: int
    members: int
    clanCapitalPoints: int
    rank: int
    previousRank: int


class ClanCapitalRankingListResponse(ItemsResponse[ClanCapitalRanking]):
    pass
