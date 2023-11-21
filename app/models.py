import datetime
from enum import Enum
from typing import List, Optional, Dict, Tuple, Union

from pydantic import BaseModel, Field


class ClientError(Exception):
	def __init__(self, reason, message, status):
		self.reason: str = reason
		self.message: str = message
		self.status: int = status


class IconUrls(BaseModel):
	small: Optional[str]
	medium: Optional[str]
	large: Optional[str]


class BadgeUrls(BaseModel):
	tiny: Optional[str]
	small: Optional[str]
	medium: Optional[str]
	large: Optional[str]

class BaseLeague(BaseModel):
	id: int
	name: str


class League(BaseLeague):
	iconUrls: IconUrls


class Label(BaseModel):
	name: str
	id: int
	iconUrls: IconUrls


class BasePlayer(BaseModel):
	tag: str
	name: str


class BaseClan(BaseModel):
	tag: str
	name: str
	clanLevel: int
	badgeUrls: BadgeUrls


class BaseCapitalDistrict(BaseModel):
	id: int
	name: str
	districtHallLevel: int


class ClanCapitalRaidSeasonAttack(BaseModel):
	attacker: BasePlayer
	destructionPercent: int
	stars: int


class ClanCapitalRaidSeasonDistrict(BaseCapitalDistrict):
	stars: int
	destructionPercent: int
	attackCount: int
	totalLooted: int
	attacks: Optional[list[ClanCapitalRaidSeasonAttack]]


class ClanCapitalRaidSeasonAttackLogEntry(BaseModel):
	defender: BaseClan
	attackCount: int
	districtCount: int
	districtsDestroyed: int
	districts: list[ClanCapitalRaidSeasonDistrict]


class ClanCapitalRaidSeasonDefenseLogEntry(BaseModel):
	attacker: BaseClan
	attackCount: int
	districtCount: int
	districtsDestroyed: int
	districts: list[ClanCapitalRaidSeasonDistrict]


class ClanCapitalRaidSeasonMember(BasePlayer):
	attacks: int
	attackLimit: int
	bonusAttackLimit: int
	capitalResourcesLooted: int


class ClanCapitalRaidSeasonState(str, Enum):
	ongoing = "ongoing"
	ended = "ended"


class Role(str, Enum):
	member = "member"
	admin = "admin"
	coLeader = "coLeader"
	leader = "leader"


class ClanCapitalRaidSeason(BaseModel):
	attackLog: Optional[list[ClanCapitalRaidSeasonAttackLogEntry]]
	defenseLog: Optional[list[ClanCapitalRaidSeasonDefenseLogEntry]]
	state: ClanCapitalRaidSeasonState
	startTime: str
	endTime: str
	capitalTotalLoot: int
	raidsCompleted: int
	totalAttacks: int
	enemyDistrictsDestroyed: int
	offensiveReward: int
	defensiveReward: int
	members: Optional[list[ClanCapitalRaidSeasonMember]]


class Location(BaseModel):
	id: int
	name: str
	isCountry: bool
	countryCode: Optional[str]


class ClanCapitalRankingClan(BaseClan):
	location: Location
	members: int
	rank: int
	previousRank: int
	clanCapitalPoints: int


class ClanMember(BasePlayer):
	league: League
	builderBaseLeague: BaseLeague
	builderBaseTrophies: int
	role: Role
	expLevel: int
	clanRank: int
	previousClanRank: int
	donations: int
	donationsReveived: int
	trophies: int
	playerHouse: PlayerHouse