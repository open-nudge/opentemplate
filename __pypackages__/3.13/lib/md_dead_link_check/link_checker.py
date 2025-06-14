from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from fnmatch import fnmatch
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client_exceptions import ClientResponseError

from md_dead_link_check.config import Config
from md_dead_link_check.preprocess import LinkInfo
from md_dead_link_check.preprocess import MarkdownInfo

TIMEOUT_RESPONSE_CODE = 408

MSG_TIMEOUT = "408: Timeout"
MSG_PATH_NOT_FOUND = "Path not found"
MSG_PATH_NOT_ADDED = "Path not added to repository"
MSG_FRAGMENT_NOT_FOUND = "Fragment not found"
MSG_UNKNOWN_ERROR = "Unknown error"
MSG_PARSING_ERROR = "Error parsing link"
IGNORED_PROTOCOLS = ("ftp", "sftp")


class Status(int, Enum):
    OK = 0
    WARNING = 1
    ERROR = 2


@dataclass
class StatusInfo:
    link_info: LinkInfo
    status: Status
    msg: Optional[str] = None

    def __lt__(self, other: StatusInfo) -> bool:
        return self.status < other.status or (self.status == other.status and self.link_info < other.link_info)


@dataclass
class LinkStatus:
    link: str
    status: Status
    msg: Optional[str] = None


@dataclass
class LinkWithDelay:
    link: str
    delay: int


async def process_link(data: LinkWithDelay, session: ClientSession, config: Config) -> LinkStatus:
    """
    Asynchronously processes a link to check its status and gather information.
    Timeout is not interpolated as error, because timeout often occur due to temporary server issues and
    retrying the request might be more appropriate than treating it as an immediate failure.
    """
    link = data.link
    delay = data.delay

    kwargs = {
        "url": link,
        "allow_redirects": True,
        "timeout": config.timeout,
        "ssl": config.validate_ssl,
    }

    try:
        # Use delay to avoid rate limiting (429: Too Many Requests)
        if delay:
            await asyncio.sleep(delay)

        if any(fnmatch(link, p) for p in config.force_get_requests_for_links):
            response = await session.get(**kwargs)
        else:
            response = await session.head(**kwargs)
            if response.status == 404:
                # Some web sites are not supports head request and return 404 code
                response = await session.get(**kwargs)
        response.raise_for_status()
    except ClientResponseError as e:
        if not config.catch_response_codes or e.status in config.catch_response_codes:
            return LinkStatus(link, Status.ERROR, f"{e.status}: {e.message}")
        return LinkStatus(link, Status.WARNING, f"{e.status}: {e.message}")
    except asyncio.CancelledError as e:
        return LinkStatus(link, Status.ERROR, str(e))
    except ClientConnectorError as e:
        return LinkStatus(link, Status.ERROR, str(e))
    except asyncio.TimeoutError:
        if TIMEOUT_RESPONSE_CODE in config.catch_response_codes:
            return LinkStatus(link, Status.ERROR, MSG_TIMEOUT)
        return LinkStatus(link, Status.WARNING, MSG_TIMEOUT)
    except Exception as e:
        msg = str(e)
        if not msg:
            msg = MSG_UNKNOWN_ERROR
        return LinkStatus(link, Status.ERROR, msg)
    return LinkStatus(link, Status.OK)


async def async_check_links(links: list[LinkWithDelay], config: Config) -> list[LinkStatus]:
    async with ClientSession(trust_env=True) as session:
        ret = await asyncio.gather(*[process_link(li, session, config) for li in links])
    return ret


def calculate_delay(counter: int, config: Config) -> int:
    return min(counter // config.throttle_groups * config.throttle_delay, config.throttle_max_delay)


def generate_delays_for_one_domain_links(links: list[str], config: Config) -> list[LinkWithDelay]:
    domain_requests_counter: dict[str, int] = defaultdict(int)
    ret: list[LinkWithDelay] = []

    for link in links:
        domain = urlsplit(link).netloc
        delay = calculate_delay(domain_requests_counter[domain], config)
        ret.append(LinkWithDelay(link, delay))
        domain_requests_counter[domain] += 1

    enabled_throttling = {d: num - 1 for d, num in domain_requests_counter.items() if num - 1 > config.throttle_groups}
    if enabled_throttling:
        print("Throttling applied to limit request frequency:")
        for domain, num_request in enabled_throttling.items():
            if num_request > config.throttle_groups:
                max_delay = calculate_delay(num_request, config)
                print(f" - Domain:         {domain}")
                print(f"   Requests count: {num_request}")
                if max_delay == config.throttle_max_delay:
                    print(f"   Maximum delay:  {max_delay} seconds (reached throttle_max_delay)")
                else:
                    print(f"   Maximum delay:  {max_delay} seconds")

    return ret


def check_web_links(md_data: dict[str, MarkdownInfo], config: Config, files: list[str]) -> list[StatusInfo]:
    ret: list[StatusInfo] = []

    web_links: list[LinkInfo] = []
    for md_file in files:
        if md_file not in md_data:
            continue
        md_file_info = md_data[md_file]
        if any(fnmatch(md_file, p) for p in config.exclude_files):
            continue
        for li in md_file_info.links:
            try:
                split_result = urlsplit(li.link)
            except ValueError:
                # Dont add error to avoid duplication error message
                continue
            if split_result.scheme in IGNORED_PROTOCOLS:
                continue
            if any(fnmatch(li.link, p) for p in config.exclude_links):
                continue
            if split_result.netloc:
                web_links.append(li)

    # Check only unique links
    unique_links = list(set(li.link for li in web_links))
    links_with_delay = generate_delays_for_one_domain_links(unique_links, config)
    links_status = asyncio.run(async_check_links(links_with_delay, config))

    links_status_dict = {li.link: li for li in links_status}

    for wl in web_links:
        li_status = links_status_dict[wl.link]
        ret.append(StatusInfo(wl, li_status.status, li_status.msg))
    return ret


def check_path_links(
    md_data: dict[str, MarkdownInfo], root_dir: Path, config: Config, files_in_repo: list[Path]
) -> list[StatusInfo]:
    ret: list[StatusInfo] = []

    for md_file, md_file_info in md_data.items():
        if any(fnmatch(md_file, p) for p in config.exclude_files):
            continue
        md_abs_path = root_dir / md_file_info.path
        for md_link in md_file_info.links:
            if md_link.link == "#":
                # Link on top of file
                continue
            if any(fnmatch(md_link.link, p) for p in config.exclude_links):
                continue

            try:
                split_result = urlsplit(md_link.link)
            except ValueError:
                ret.append(StatusInfo(md_link, Status.ERROR, MSG_PARSING_ERROR))
                continue

            if split_result.scheme or split_result.netloc:
                continue
            fragment = split_result.fragment.lower()

            if not split_result.path:
                if fragment not in md_file_info.fragments:
                    ret.append(StatusInfo(md_link, Status.ERROR, MSG_FRAGMENT_NOT_FOUND))
                    continue
            else:
                try:
                    if split_result.path.startswith("/"):
                        # path from git root dir
                        abs_path = root_dir / split_result.path[1:]
                        rel_path = Path(split_result.path[1:])
                    else:
                        abs_path = (md_abs_path.parent / split_result.path).resolve()
                        rel_path = abs_path.relative_to(root_dir)
                except ValueError:
                    ret.append(StatusInfo(md_link, Status.ERROR, MSG_PATH_NOT_FOUND))
                    continue

                if abs_path.as_posix() != abs_path.resolve().as_posix():
                    ret.append(StatusInfo(md_link, Status.ERROR, MSG_PATH_NOT_FOUND))
                    continue

                if rel_path.as_posix() in md_data:
                    # Markdowns in repository
                    if fragment and fragment not in md_data[rel_path.as_posix()].fragments:
                        ret.append(StatusInfo(md_link, Status.ERROR, MSG_FRAGMENT_NOT_FOUND))
                        continue
                else:
                    # Not markdown file
                    if not any(f.as_posix().startswith(rel_path.as_posix()) for f in files_in_repo):
                        if rel_path.exists():
                            ret.append(StatusInfo(md_link, Status.ERROR, MSG_PATH_NOT_ADDED))
                        else:
                            ret.append(StatusInfo(md_link, Status.ERROR, MSG_PATH_NOT_FOUND))
                        continue

            ret.append(StatusInfo(md_link, Status.OK))
    return ret


def check_all_links(
    md_data: dict[str, MarkdownInfo], config: Config, root_dir: Path, files: list[str], files_in_repo: list[Path]
) -> list[StatusInfo]:
    status_list: list[StatusInfo] = []
    if config.check_web_links:
        status_list.extend(check_web_links(md_data, config, files))
    status_list.extend(check_path_links(md_data, root_dir, config, files_in_repo))
    return sorted(status_list)
