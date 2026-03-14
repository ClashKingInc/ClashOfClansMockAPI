from pydantic import Field

from .common import (
    ApiModel,
    BadgeUrls,
    BuilderBaseLeague,
    ClanReference,
    ItemsResponse,
    Label,
    League,
    LeagueTier,
    PlayerAchievementProgress,
    PlayerClan,
    PlayerHouse,
    PlayerItemLevel,
    PlayerLegendStatistics,
    Resource,
)


class Player(ApiModel):
    tag: str
    name: str
    townHallLevel: int
    expLevel: int
    trophies: int
    bestTrophies: int
    warStars: int
    attackWins: int
    defenseWins: int
    builderHallLevel: int | None = None
    builderBaseTrophies: int | None = None
    bestBuilderBaseTrophies: int | None = None
    role: str | None = None
    warPreference: str | None = None
    donations: int | None = None
    donationsReceived: int | None = None
    clanCapitalContributions: int | None = None
    clan: PlayerClan | None = None
    league: League | None = None
    leagueTier: LeagueTier | None = None
    builderBaseLeague: BuilderBaseLeague | None = None
    currentLeagueGroupTag: str | None = None
    currentLeagueSeasonId: int | None = None
    previousLeagueGroupTag: str | None = None
    previousLeagueSeasonId: int | None = None
    legendStatistics: PlayerLegendStatistics | None = None
    achievements: list[PlayerAchievementProgress] = Field(default_factory=list)
    playerHouse: PlayerHouse | None = None
    labels: list[Label] = Field(default_factory=list)
    troops: list[PlayerItemLevel] = Field(default_factory=list)
    heroes: list[PlayerItemLevel] = Field(default_factory=list)
    heroEquipment: list[PlayerItemLevel] = Field(default_factory=list)
    spells: list[PlayerItemLevel] = Field(default_factory=list)


class BattleLogEntry(ApiModel):
    battleType: str
    attack: bool
    armyShareCode: str | None = None
    opponentPlayerTag: str
    stars: int
    destructionPercentage: int
    lootedResources: list[Resource] = Field(default_factory=list)
    extraLootedResources: list[Resource] = Field(default_factory=list)
    availableLoot: list[Resource] = Field(default_factory=list)


class BattleLogResponse(ItemsResponse[BattleLogEntry]):
    pass


class PlayerRanking(ApiModel):
    tag: str
    name: str
    expLevel: int
    rank: int
    previousRank: int
    trophies: int
    attackWins: int | None = None
    defenseWins: int | None = None
    clan: ClanReference | None = None
    league: League | None = None
    leagueTier: LeagueTier | None = None


class PlayerRankingListResponse(ItemsResponse[PlayerRanking]):
    pass


class PlayerBuilderBaseRanking(ApiModel):
    tag: str
    name: str
    expLevel: int
    rank: int
    previousRank: int
    builderBaseTrophies: int
    clan: ClanReference | None = None
    builderBaseLeague: BuilderBaseLeague | None = None


class PlayerBuilderBaseRankingListResponse(ItemsResponse[PlayerBuilderBaseRanking]):
    pass
