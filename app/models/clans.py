
from pydantic import Field

from .common import (
    ApiModel,
    BadgeUrls,
    CapitalLeague,
    ClanReference,
    ItemsResponse,
    Label,
    Language,
    League,
    Location,
    PlayerClan,
    PlayerHouse,
    PlayerTag,
    WarLeague,
)
from .leagues import ClanWarLeagueGroup


class ClanMember(ApiModel):
    tag: str
    name: str
    role: str
    expLevel: int
    league: League | None = None
    trophies: int
    builderBaseTrophies: int | None = None
    versusTrophies: int | None = None
    clanRank: int
    previousClanRank: int
    donations: int
    donationsReceived: int
    playerHouse: PlayerHouse | None = None
    builderBaseLeague: League | None = None


class ClanMembersResponse(ItemsResponse[ClanMember]):
    pass


class ClanCapitalDistrict(ApiModel):
    id: int
    name: str
    districtHallLevel: int


class ClanCapital(ApiModel):
    capitalHallLevel: int | None = None
    districts: list[ClanCapitalDistrict] = Field(default_factory=list)


class Clan(ApiModel):
    tag: str
    name: str
    type: str
    description: str | None = None
    location: Location | None = None
    isFamilyFriendly: bool | None = None
    badgeUrls: BadgeUrls | None = None
    clanLevel: int
    clanPoints: int
    clanBuilderBasePoints: int | None = None
    clanVersusPoints: int | None = None
    clanCapitalPoints: int | None = None
    capitalLeague: CapitalLeague | None = None
    requiredTrophies: int | None = None
    warFrequency: str | None = None
    warWinStreak: int | None = None
    warWins: int | None = None
    warTies: int | None = None
    warLosses: int | None = None
    isWarLogPublic: bool | None = None
    warLeague: WarLeague | None = None
    members: int
    memberList: list[ClanMember] = Field(default_factory=list)
    labels: list[Label] = Field(default_factory=list)
    requiredBuilderBaseTrophies: int | None = None
    requiredVersusTrophies: int | None = None
    requiredTownhallLevel: int | None = None
    clanCapital: ClanCapital | None = None
    chatLanguage: Language | None = None


class ClanSearchItem(ApiModel):
    tag: str
    name: str
    type: str
    location: Location | None = None
    isFamilyFriendly: bool | None = None
    badgeUrls: BadgeUrls | None = None
    clanLevel: int
    clanPoints: int
    clanBuilderBasePoints: int | None = None
    clanVersusPoints: int | None = None
    clanCapitalPoints: int | None = None
    capitalLeague: CapitalLeague | None = None
    requiredTrophies: int | None = None
    warFrequency: str | None = None
    warWinStreak: int | None = None
    warWins: int | None = None
    warTies: int | None = None
    warLosses: int | None = None
    isWarLogPublic: bool | None = None
    warLeague: WarLeague | None = None
    members: int
    labels: list[Label] = Field(default_factory=list)
    requiredBuilderBaseTrophies: int | None = None
    requiredVersusTrophies: int | None = None
    requiredTownhallLevel: int | None = None
    chatLanguage: Language | None = None


class ClanSearchResponse(ItemsResponse[ClanSearchItem]):
    pass


class ClanWarAttack(ApiModel):
    attackerTag: str
    defenderTag: str
    stars: int
    destructionPercentage: int
    order: int
    duration: int | None = None


class ClanWarMember(ApiModel):
    tag: str
    name: str
    townhallLevel: int
    mapPosition: int
    attacks: list[ClanWarAttack] = Field(default_factory=list)
    opponentAttacks: int | None = None
    bestOpponentAttack: ClanWarAttack | None = None


class WarClan(ApiModel):
    tag: str
    name: str
    badgeUrls: BadgeUrls | None = None
    clanLevel: int
    attacks: int | None = None
    stars: int | None = None
    destructionPercentage: float | None = None
    expEarned: int | None = None
    members: list[ClanWarMember] = Field(default_factory=list)


class ClanWar(ApiModel):
    state: str
    teamSize: int | None = None
    attacksPerMember: int | None = None
    battleModifier: str | None = None
    preparationStartTime: str | None = None
    startTime: str | None = None
    endTime: str | None = None
    clan: WarClan | None = None
    opponent: WarClan | None = None


class ClanWarLogEntry(ApiModel):
    result: str | None = None
    endTime: str
    teamSize: int
    attacksPerMember: int | None = None
    battleModifier: str | None = None
    clan: WarClan
    opponent: WarClan


class ClanWarLogResponse(ItemsResponse[ClanWarLogEntry]):
    pass


class ClanCapitalRaidSeasonAttacker(PlayerTag):
    pass


class ClanCapitalRaidSeasonAttack(ApiModel):
    attacker: ClanCapitalRaidSeasonAttacker
    destructionPercent: int
    stars: int


class ClanCapitalRaidSeasonDistrict(ApiModel):
    id: int
    name: str
    districtHallLevel: int
    destructionPercent: int
    stars: int
    attackCount: int
    totalLooted: int
    attacks: list[ClanCapitalRaidSeasonAttack] = Field(default_factory=list)


class ClanCapitalRaidSeasonClanInfo(ApiModel):
    tag: str
    name: str
    level: int
    badgeUrls: BadgeUrls | None = None


class ClanCapitalRaidSeasonAttackLogEntry(ApiModel):
    defender: ClanCapitalRaidSeasonClanInfo
    attackCount: int
    districtCount: int
    districtsDestroyed: int
    districts: list[ClanCapitalRaidSeasonDistrict] = Field(default_factory=list)


class ClanCapitalRaidSeasonDefenseLogEntry(ApiModel):
    attacker: ClanCapitalRaidSeasonClanInfo
    attackCount: int
    districtCount: int
    districtsDestroyed: int
    districts: list[ClanCapitalRaidSeasonDistrict] = Field(default_factory=list)


class ClanCapitalRaidSeasonMember(PlayerTag):
    attacks: int
    attackLimit: int
    bonusAttackLimit: int
    capitalResourcesLooted: int


class ClanCapitalRaidSeason(ApiModel):
    state: str
    startTime: str
    endTime: str
    capitalTotalLoot: int
    raidsCompleted: int
    totalAttacks: int
    enemyDistrictsDestroyed: int
    offensiveReward: int
    defensiveReward: int
    members: list[ClanCapitalRaidSeasonMember] = Field(default_factory=list)
    attackLog: list[ClanCapitalRaidSeasonAttackLogEntry] = Field(default_factory=list)
    defenseLog: list[ClanCapitalRaidSeasonDefenseLogEntry] = Field(default_factory=list)


class CapitalRaidSeasonsResponse(ItemsResponse[ClanCapitalRaidSeason]):
    pass
