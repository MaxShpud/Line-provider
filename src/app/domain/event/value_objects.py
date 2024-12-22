import enum

class EventStatusEnum(enum.Enum):
    UNFINISHED = 'UNFINISHED'
    WON = 'WON'
    LOST = 'LOST'

class EventTypeEnum(enum.Enum):
    NONE = "NONE"
    SPORT = "SPORT"
    CYBER_SPORT = "CYBERSPORT"
