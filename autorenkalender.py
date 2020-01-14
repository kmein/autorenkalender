from typing import Optional, Generator
from datetime import date, datetime
import re
import sys

import requests

AUTORENKALENDER_URL = "https://www.projekt-gutenberg.org/info/kalender/autoren.js"

AUTHOR_URL_BASE = "https://www.projekt-gutenberg.org/autoren/namen/"

AUTHOR_REGEX = re.compile(r"^Autor\(")
LINE_REGEX = re.compile(
    r'^Autor\("'
    r'(?P<last_name>.*)",'
    r'"(?P<first_name>.*)",'
    r'"(?P<birth_string>\d{8})",'
    r'"(?P<death_string>\d{8})",'
    r'"(?P<url>.*html)"\);$'
)


def parse_date(string: str) -> Optional[date]:
    try:
        return datetime.strptime(string, "%Y%m%d").date()
    except ValueError:
        return None


class Author:
    last_name: str
    first_name: str
    birth: Optional[date]
    death: Optional[date]
    url: str

    def __init__(self, line: str):
        match = LINE_REGEX.match(line)
        if match:
            birth_string = match.group("birth_string")
            death_string = match.group("death_string")

            self.url = AUTHOR_URL_BASE + match.group("url")
            self.last_name = match.group("last_name")
            self.first_name = match.group("first_name")
            self.birth = parse_date(birth_string)
            self.death = parse_date(death_string)
        else:
            raise ValueError(f'"{line}" could not be extracted.')

    def birthday_today(self) -> Optional[int]:
        today = date.today()
        if (
            self.birth
            and self.birth.day == today.day
            and self.birth.month == today.month
        ):
            return today.year - self.birth.year
        return None

    def deathday_today(self) -> Optional[int]:
        today = date.today()
        if (
            self.death
            and self.death.day == today.day
            and self.death.month == today.month
        ):
            return today.year - self.death.year
        return None

    def print_info(self) -> None:
        years_alive = self.birthday_today()
        years_dead = self.deathday_today()

        if years_alive or years_dead:
            print(
                "[{name}]({url}]".format(
                    name=self.first_name.strip() + " " + self.last_name.strip(),
                    url=self.url,
                )
            )
            if years_alive:
                print("{}. Geburtstag".format(years_alive))
            if years_dead:
                print("{}. Todestag".format(years_dead))
            print()


def author_lines() -> Generator[str, None, None]:
    """Returns the text of the Autorenkalender JavaScript file"""
    response = requests.get(AUTORENKALENDER_URL)
    if response.status_code == 200:
        for line in response.text.splitlines():
            if AUTHOR_REGEX.search(line):
                yield line


if __name__ == "__main__":
    for author_line in author_lines():
        try:
            author = Author(author_line)
            author.print_info()
        except ValueError:
            pass
