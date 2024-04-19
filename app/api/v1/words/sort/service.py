import logging

from app.api.v1.words.sort.exceptions import SortWordsException
from app.api.v1.words.sort.models import (
    SortWordsRequest,
    SortWordsResponse,
)

logger = logging.getLogger(__name__)


class SortWordService:
    def __init__(self) -> None:
        self.ASCENDING = "asc"
        self.DESCENDING = "desc"

    def sort_words(self, sort_words: SortWordsRequest) -> SortWordsResponse:
        try:
            match sort_words.order:
                case self.ASCENDING:
                    sort_words.words.sort()
                    return sort_words.words
                case self.DESCENDING:
                    sort_words.words.sort(reverse=True)
                    return sort_words.words
                case _:
                    return sort_words.words
        except Exception as error:
            logger.error("Unmapped error in SortWordService", extra={"error": error})
            raise SortWordsException()
