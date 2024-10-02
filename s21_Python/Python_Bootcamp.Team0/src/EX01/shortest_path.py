from typing import Tuple, List, Set, Dict
import argparse
import os
import json
import sys


def get_args() -> Tuple[Dict[str, str], Dict[str, bool]]:
    """
    Parse command line arguments into start and end pages and flags
    """
    start: str = 'start'
    end: str = 'end'
    undirect: str = 'undirect'
    view: str = 'view'

    description_str: str = 'The script gives the shortest path between two wiki pages'
    help_start: str = 'write after flag start_page title'
    help_end: str = 'write after flag end_page title'
    help_undirect: str = 'every edge is treated equal in both directions'
    help_view: str = 'enable logging of the found path'

    parser = argparse.ArgumentParser(description=description_str)

    parser.add_argument('--from', dest=start, required=True, help=help_start)
    parser.add_argument('--to', dest=end, required=True,  help=help_end)
    parser.add_argument('--non-directed', dest=undirect, action='store_true',
                        help=help_undirect)
    parser.add_argument('-v', dest=view, action='store_true', help=help_view)

    args = parser.parse_args()

    pages: Dict[str, str] = {start: args.start, end: args.end}
    flags: Dict[str, bool] = {undirect: args.undirect, view: args.view}
    return pages, flags


def json_handle(file_path: str, pages: Dict[str, str],
                flags: Dict[str, bool]) -> None:
    """
    JSON load and sending to parsing
    """
    with open(file_path, 'r') as file:
        data: dict | None = json.loads(file.read())
    if data:
        if (pages_check(data, pages, flags)):
            search_path(data, pages, flags)
        else:
            raise ValueError('page not in data')
    else:
        raise ValueError('error opening json')


def pages_check(data: Dict[str, List[str]], pages: Dict[str, str],
                flags: Dict[str, bool]) -> bool:
    """
    Check for start and end pages in data
    """
    exist_start: bool = False
    exist_end: bool = False
    for source, links in data.items():
        if not exist_start and pages["start"] == source:
            exist_start = True
        elif not exist_end and pages["end"] == source:
            exist_end = True
        elif flags["undirect"]:
            if not exist_start and pages["start"] in links:
                exist_start = True
            elif not exist_end and pages["end"] in links:
                exist_end = True
        if exist_start and exist_end:
            break
    return exist_start and exist_end
    

def search_path(data: Dict[str, List[str]], pages: Dict[str, str],
                flags: Dict[str, bool]) -> None:
    """
    Path from start to end page
    """
    path: List[str] = []
    queue: List[str] = [pages['start']]
    visited: Set[str] = set()
    flags['find'] = False
    flags['no_path'] = False
    cr: int = 0
    cr_range: int = 200
    while (queue and not flags['find'] and not flags['no_path']):
        node = queue.pop(0)
        if node not in data and flags['undirect']:
            data[node] = []
        if node not in visited and node in data:
            visited.add(node)
            if pages['end'] in data[node] or pages['end'] == node:
                flags['find'] = True
                path = reverse_path(data, node, pages)
                print() if cr > cr_range and flags['view'] else None
                print_view(path) if flags['view'] else None
            else:
                collect_targets(data, node) if flags['undirect'] else None
                append_source_and_queue(data, node, visited, queue)
                cr += 1
                if cr % cr_range == 0:
                    sys.stdout.flush()
                    sys.stdout.write(f"\rCheck {cr} pages")
    print() if cr > cr_range and not flags['view'] else None
    print(len(path) - 1) if flags['find'] else print('path not found')


def reverse_path(data: Dict[str, List[str]], prev: str,
                 pages: Dict[str, str]) -> List[str]:
    """
    Finding a path by an appending source, walking from end to start
    """
    len_src = len("source: ")
    path: List[str] = []
    if prev != pages['end']:
        path.append(pages['end'])
    node: str = prev
    while (node != pages['start']):
        path.append(node)
        if is_source_node(data, node):
            node = data[node][-1][len_src:]
        else:
            raise ValueError("source not added")
    path.append(pages['start'])
    return path


def print_view(path: List[str]) -> None:
    """
    Output shortest path from start page to end page
    """
    for i in range(len(path) - 1, -1, -1):
        print(path[i], end='')
        if i:
            print(' -> ', end='')
        else:
            print()


def collect_targets(data: Dict[str, List[str]], node: str) -> None:
    """
    Collect node containing targets
    """
    for target, links in data.items():
        if node in links and target not in data[node]:
            if is_source_node(data, node):
                data[node].insert(-1, target)
            else:
                data[node].append(target)


def is_source_node(data: Dict[str, List[str]], target: str) -> bool:
    return len(data[target]) > 0 and data[target][-1].startswith("source: ")


def append_source_and_queue(data: Dict[str, List[str]], node: str,
                            visited: Set[str], queue: List[str]) -> None:
    """
    Append source node to target links 
    and append target to the search queue
    """
    src_appendix: str = "source: "
    for target in data[node]:
        if target in data:                
            if not is_source_node(data, target):
                data[target].append(src_appendix + node)
        else:
            data[target] = [src_appendix + node]
        if target not in queue and target not in visited \
            and not target.startswith("source: "): 
            queue.append(target)


if __name__ == '__main__':
    pages, flags = get_args()
    file_path: str | None = os.getenv('WIKI_FILE')
    if file_path:
        try:
            json_handle(file_path, pages, flags)
        except FileNotFoundError:
            print('database not found')
        except ValueError as e:
            print(e)  
    else:
        print('environment file not found')
