
from .common import ApiModel, ItemsResponse, Label


class LabelListResponse(ItemsResponse[Label]):
    pass


class GoldPassSeason(ApiModel):
    startTime: str
    endTime: str
