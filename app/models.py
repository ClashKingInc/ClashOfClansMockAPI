import datetime
from enum import Enum
from typing import List, Optional, Dict, Tuple, Union

from pydantic import BaseModel, Field


class ClientError(BaseModel, Exception):
	reason: str
	message: str
	status: int


class WarLeague(BaseModel):
	id: int
	name: str


class IconUrls(BaseModel):
	small: Optional[str]
	medium: Optional[str]
	large: Optional[str]


class BadgeUrls(BaseModel):
	tiny: Optional[str]
	small: Optional[str]
	medium: Optional[str]
	large: Optional[str]


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
	level: int
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



