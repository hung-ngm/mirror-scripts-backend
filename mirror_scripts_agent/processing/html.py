"""HTML processing functions"""
from __future__ import annotations

from bs4 import BeautifulSoup
from requests.compat import urljoin


def extract_hyperlinks(soup: BeautifulSoup, base_url: str) -> list[tuple[str, str]]:
    """
    Extract hyperlinks from a BeautifulSoup object

    Args:
        soup (BeautifulSoup): BeautifulSoup object
        base_url (str): Base URL to use for relative links

    Returns:
        list[tuple[str, str]]: List of hyperlinks extracted
    """
    return [
        (link.text, urljoin(base_url, link["href"]))
        for link in soup.find_all("a", href=True)
    ]

def format_hyperlinks(hyperlinks: list[tuple[str, str]]) -> list[str]:
    """
    Format hyperlinks to be displayed to the user

    Args:
        hyperlinks (List[Tuple[str, str]]): List of hyperlinks to format

    Returns:
        List[str]: The formatted hyperlinks
    """
    return [f"{link_text} ({link_url})" for link_text, link_url in hyperlinks]