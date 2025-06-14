from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from git import Repo

RE_HEADER = r"^(?:\s*[-+*]\s+|)[#]{1,6}\s*(.*?)\s*[#]*$"
RE_URL = r"(http[s]?://[^>)\]\s\"]+)"
RE_LINK = r"([!]{0,1})\[([^\]!]*)\]\(([^()\s]+(?:\([^()\s]*\))*)\s*(.*?)\)"
RE_HTML_TAG = r"</?\w+[^>]*>"
RE_HTML_TAG_ID = r"<\w+\s+(?:[^>]*?\s+)?(?:id|name)=([\"'])(.*?)\1"
RE_HTML_TAG_HREF = r"<\w+\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\1"
RE_SUB = r"[$`][^`]+?[$`]"

MD_TAG_DISABLE = "<!-- md-dead-link-check: off -->"
MD_TAG_ENABLE = "<!-- md-dead-link-check: on -->"


@dataclass
class LinkInfo:
    link: str
    location: Path
    line_num: int

    def get_location(self) -> str:
        """
        Returns location link in format path:line
        """
        return f"{self.location}:{self.line_num}"

    def __lt__(self, other: LinkInfo) -> bool:
        return self.location < other.location or (self.location == other.location and self.line_num < other.line_num)


@dataclass
class MarkdownInfo:
    path: Path
    fragments: list[str] = field(default_factory=lambda: [])
    links: list[LinkInfo] = field(default_factory=lambda: [])


def find_all_markdowns(all_files: list[str]) -> list[Path]:
    """
    Filter markdown files.
    """
    ret = []
    for file_path in all_files:
        p = Path(file_path)
        if p.suffix == ".md":
            ret.append(p)
    return ret


def process_header_to_fragment(header: str) -> str:
    """
    Converts a Markdown header to a URL fragment.
    """

    fragment = header.strip()
    fragment = re.sub(RE_HTML_TAG, "", fragment)
    while True:
        res = re.search(RE_LINK, fragment)
        if not res:
            break
        if res.group(1) == "!":
            # Use # to work
            fragment = fragment.replace(res.group(0), "")
        else:
            fragment = fragment.replace(res.group(0), res.group(2))

    fragment = fragment.lower().replace(" ", "-")

    def filter_header_symbols(c: str) -> bool:
        return c.isalpha() or c.isdigit() or c in ["-", "_"]

    fragment = "".join(filter(filter_header_symbols, fragment))
    return fragment


def process_md_file(path: Path, root_dir: Path) -> MarkdownInfo:
    fragments: list[str] = []
    links: list[LinkInfo] = []
    with (root_dir / path).open(encoding="utf8") as stream:
        in_code_block = ""
        disable_detection_links = False
        for line_num, line in enumerate(stream.readlines(), 1):
            striped_line = line.strip()
            # Skip code blocks that can be start ``` or ````
            res = re.match(r"^(`{3,4})(.+)`{3,4}\s*$", striped_line)
            if res:
                continue
            res = re.match(r"^(`{3,4})", striped_line)
            if res and not in_code_block:
                in_code_block = res.group(1)
                continue
            if striped_line.startswith(in_code_block):
                in_code_block = ""
            if in_code_block:
                continue

            # Detect headers
            res = re.match(RE_HEADER, line)
            if res:
                _fragment = process_header_to_fragment(res.group(1))
                fragment = _fragment
                repeat = 0
                while fragment in fragments:
                    repeat += 1
                    fragment = f"{_fragment}-{repeat}"
                fragments.append(fragment)

            # Skip $ and ` tags
            line = re.sub(RE_SUB, "", line)

            # Detect id under a tag <a id="introduction"></a>
            matches = re.findall(RE_HTML_TAG_ID, line)
            for _, id in matches:
                fragments.append(id.lower())

            if MD_TAG_DISABLE in line:
                disable_detection_links = True
                continue

            if MD_TAG_ENABLE in line:
                disable_detection_links = False
                continue

            if disable_detection_links:
                continue

            # Detect links
            copy_line = line  # Used to detect bare links
            matches = re.findall(RE_LINK, line)
            for img_tag, text, link, title in matches:
                links.append(LinkInfo(link, path, line_num))
                copy_line = copy_line.replace(link, "")

            if matches:
                # For case [![text](img_link)](link)
                sub_line = re.sub(RE_LINK, "link", line)
                matches2 = re.findall(RE_LINK, sub_line)
                for img_tag, text, link, title in matches2:
                    links.append(LinkInfo(link, path, line_num))
                    copy_line = copy_line.replace(link, "")

            # Detect links under a tag <a href="introduction"></a>
            matches = re.findall(RE_HTML_TAG_HREF, line)
            for _, link in matches:
                links.append(LinkInfo(link, path, line_num))
                copy_line = copy_line.replace(link, "")

            # Detect simple urls without any tags
            matches = re.findall(RE_URL, copy_line)
            for url in matches:
                url = re.sub(r"[,.:]+$", "", url)
                links.append(LinkInfo(url, path, line_num))

    return MarkdownInfo(path=path, fragments=fragments, links=links)


def preprocess_repository(untracked_files: bool) -> tuple[dict[str, MarkdownInfo], Path, list[Path]]:
    repo = Repo(search_parent_directories=True)
    root_dir = Path(repo.working_dir)

    all_files: list[str] = repo.git.ls_files().splitlines()
    if untracked_files:
        all_files += repo.untracked_files

    list_md_files = find_all_markdowns(all_files)
    md_data = {}
    for md_file in list_md_files:
        md_info = process_md_file(md_file, root_dir)
        md_data[md_file.as_posix()] = md_info

    files_in_repo = [Path(x) for x in all_files]
    return md_data, root_dir, files_in_repo
