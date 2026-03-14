
from pydantic import Field

from .common import (
    ApiModel,
    BadgeUrls,
    BuilderBaseLeague,
    CapitalLeague,
    ClanReference,
    ItemsResponse,
    League,
    LeagueTier,
    PlayerTag,
    WarLeague,
)


class LeagueSeason(ApiModel):
    id: str


class LeagueSeasonListResponse(ItemsResponse[LeagueSeason]):
    pass


class LeagueTierListResponse(ItemsResponse[LeagueTier]):
    pass


class BuilderBaseLeagueListResponse(ItemsResponse[BuilderBaseLeague]):
    pass


class CapitalLeagueListResponse(ItemsResponse[CapitalLeague]):
    pass


class WarLeagueListResponse(ItemsResponse[WarLeague]):
    pass


class LeagueSeasonResult(ApiModel):
    leagueSeasonId: int | str
    leagueTrophies: int
    leagueTierId: int
    placement: int
    attackWins: int
    attackLosses: int
    attackStars: int
    defenseWins: int
    defenseLosses: int
    defenseStars: int
    maxBattles: int


class LeagueHistoryResponse(ItemsResponse[LeagueSeasonResult]):
    pass


class LeagueBattleLogEntry(ApiModel):
    opponentPlayerTag: str
    opponentName: str
    stars: int
    destructionPercentage: int
    trophies: int
    creationTime: str


class LeagueGroupMember(ApiModel):
    playerTag: str
    playerName: str
    clanTag: str
    clanName: str
    leagueTrophies: int
    attackWinCount: int
    attackLoseCount: int
    defenseWinCount: int
    defenseLoseCount: int


class LeagueGroup(ApiModel):
    members: list[LeagueGroupMember] = Field(default_factory=list)
    attackLogs: list[LeagueBattleLogEntry] = Field(default_factory=list)
    defenseLogs: list[LeagueBattleLogEntry] = Field(default_factory=list)


class ClanWarLeagueRound(ApiModel):
    warTags: list[str] = Field(default_factory=list)


class ClanWarLeagueClanMember(PlayerTag):
    townHallLevel: int


class ClanWarLeagueClan(ApiModel):
    tag: str
    clanLevel: int
    name: str
    members: list[ClanWarLeagueClanMember] = Field(default_factory=list)
    badgeUrls: BadgeUrls | None = None


class ClanWarLeagueGroup(ApiModel):
    tag: str | None = None
    state: str
    season: str | None = None
    clans: list[ClanWarLeagueClan] = Field(default_factory=list)
    rounds: list[ClanWarLeagueRound] = Field(default_factory=list)
