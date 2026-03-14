
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


class ApiModel(BaseModel):
    pass


class CursorPaging(ApiModel):
    before: str | None = None
    after: str | None = None


class Paging(ApiModel):
    cursors: CursorPaging = Field(default_factory=CursorPaging)


class IconUrls(ApiModel):
    tiny: str | None = None
    small: str | None = None
    medium: str | None = None
    large: str | None = None


class BadgeUrls(ApiModel):
    small: str | None = None
    medium: str | None = None
    large: str | None = None


class Location(ApiModel):
    id: int
    name: str
    isCountry: bool
    countryCode: str | None = None
    localizedName: str | None = None


class Language(ApiModel):
    id: int
    name: str
    languageCode: str


class LeagueBase(ApiModel):
    id: int
    name: str


class League(LeagueBase):
    iconUrls: IconUrls | None = None


class LeagueTier(League):
    pass


class BuilderBaseLeague(LeagueBase):
    pass


class CapitalLeague(LeagueBase):
    pass


class WarLeague(LeagueBase):
    pass


class Label(ApiModel):
    id: int
    name: str
    iconUrls: IconUrls | None = None


class PlayerTag(ApiModel):
    tag: str
    name: str


class ClanTag(ApiModel):
    tag: str
    name: str


class RankedClan(ClanTag):
    badgeUrls: BadgeUrls | None = None


class ClanReference(RankedClan):
    clanLevel: int | None = None


class PlayerClan(RankedClan):
    clanLevel: int | None = None


class PlayerHouseElement(ApiModel):
    id: int
    type: str


class PlayerHouse(ApiModel):
    elements: list[PlayerHouseElement] = Field(default_factory=list)


class Resource(ApiModel):
    name: str
    amount: int


class PlayerAchievementProgress(ApiModel):
    stars: int
    value: int
    name: str
    target: int
    info: str | None = None
    completionInfo: str | None = None
    village: str


class PlayerItemLevel(ApiModel):
    name: str
    level: int
    maxLevel: int
    village: str
    superTroopIsActive: bool | None = None
    equipment: list["PlayerItemLevel"] | None = None


class LegendLeagueTournamentSeasonResult(ApiModel):
    id: str | None = None
    rank: int | None = None
    trophies: int | None = None


class PlayerLegendStatistics(ApiModel):
    currentSeason: LegendLeagueTournamentSeasonResult | None = None
    previousSeason: LegendLeagueTournamentSeasonResult | None = None
    previousBuilderBaseSeason: LegendLeagueTournamentSeasonResult | None = None
    bestBuilderBaseSeason: LegendLeagueTournamentSeasonResult | None = None
    legendTrophies: int | None = None
    bestSeason: LegendLeagueTournamentSeasonResult | None = None


T = TypeVar("T")


class ItemsResponse(ApiModel, Generic[T]):
    items: list[T]
    paging: Paging | None = None


JsonDict = dict[str, Any]
