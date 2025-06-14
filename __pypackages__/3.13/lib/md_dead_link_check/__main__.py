from argparse import ArgumentParser
from argparse import Namespace
from argparse import RawTextHelpFormatter
from pathlib import Path

from md_dead_link_check.config import get_config
from md_dead_link_check.helpers import normalize_files
from md_dead_link_check.helpers import summary
from md_dead_link_check.link_checker import check_all_links
from md_dead_link_check.preprocess import preprocess_repository


def args_parser() -> Namespace:
    parser = ArgumentParser(
        description="Checks for broken links (dead links) in a Markdown file within a Git repository.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "files",
        nargs="*",
        help=(
            "List of files to check for web links."
            "\nIf no files are provided (empty list) and the --hook flag is not used, "
            "then all markdown files in the current directory will be checked."
            "\nNote: Internal links within the files will always be checked, regardless of the "
            "provided files, to detect broken links to removed files."
        ),
    )
    parser.add_argument("--config", "-c", type=Path, help="Path to config file.")
    parser.add_argument(
        "--hook",
        action="store_true",
        help=(
            "Run program in pre-commit hook. If not pass list of files, web links will no check, "
            "by default will check in all files."
        ),
    )
    parser.add_argument("--warn", "-w", action="store_true", help="Show warning messages.")
    parser.add_argument("--all", "-a", action="store_true", help="Show all links.")
    parser.add_argument("--no-color", "-nc", action="store_true", help="Disable coloring of output.")
    parser.add_argument("--untrack", action="store_true", help="Check untracked files.")
    return parser.parse_args()


def main() -> int:
    args = args_parser()

    md_data, repo_dir, files_in_repo = preprocess_repository(untracked_files=args.untrack)
    config = get_config(repo_dir, args.config)

    files = normalize_files(args.files, repo_dir)
    if not args.hook and not files:
        files = list(md_data)

    status_list = check_all_links(md_data, config, repo_dir, files, files_in_repo)
    err_num = summary(status_list, args.warn, args.all, args.no_color)

    return min(err_num, 1)


if __name__ == "__main__":
    raise SystemExit(main())
