import logging
from collections import Counter
from types import SimpleNamespace

from unidecode import unidecode

from app.api.v1.words.vowel_count.exceptions import VowelCountException
from app.api.v1.words.vowel_count.models import VowelCountResponse

logger = logging.getLogger(__name__)


VOWELS = SimpleNamespace(A="a", E="e", I="i", O="o", U="u")


class VowelCountService:

    def return_total_vowels(self, words: list[str]) -> VowelCountResponse:
        """
        verify the total vowels existing in each word passed in the param.

        :param words: list[str], contains a list of words to verify the
        total vowels existing in each word passed.
        """
        response = {}
        try:
            for word in words:
                decode_word = unidecode(word)
                word_count = Counter(decode_word)
                count = sum(
                    [
                        word_count[VOWELS.A],
                        word_count[VOWELS.E],
                        word_count[VOWELS.I],
                        word_count[VOWELS.O],
                        word_count[VOWELS.U],
                    ]
                )
                response.update({word: count})
        except Exception as error:
            logger.error("Unmapped error in VowelCountService", extra={"error": error})
            raise VowelCountException()
        return response
