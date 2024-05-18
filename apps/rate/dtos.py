from dataclasses import dataclass
from datetime import datetime


@dataclass(init=True)
class RateRedisObjectDTO:
    rater_id: int
    post_id: int
    score: int
    created_at: datetime

    def to_dict(self):
        return {**self.__dict__, 'created_at': str(self.created_at)}
