from filler import Filler, RetryException
import time


class Miner:
    """
    Wrapper for a filler that repeatedly tries the filler,
    retrying after a given number of seconds.
    """

    def __init__(self, filler: Filler, retry_seconds: int):
        self.filler = filler
        self.retry_seconds = retry_seconds

    def fill(self, crossword_maker, wordlist, animate, continuous=False):
        retries = 0

        while True:
            retry_time = time.time() + self.retry_seconds
            crossword = crossword_maker()

            try:
                self.filler.fill(crossword, wordlist, animate, retry_time)
                if continuous:
                    print(crossword)
                else:
                    break
            except RetryException:
                retries += 1
                print(f'Attempt #{retries} timed out. Retrying.')

        print(crossword)
