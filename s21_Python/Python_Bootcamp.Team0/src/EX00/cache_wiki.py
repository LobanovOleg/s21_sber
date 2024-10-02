import argparse
import logging
import requests
import urllib.parse
from bs4 import BeautifulSoup
import networkx as nx
import json
from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable, ClientError
from typing import List, Tuple, Set
import os

logging.basicConfig(level=logging.INFO)

JSON_FILENAME = 'wiki_graph.json'

COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

MAX_PAGES = 1000
MIN_PAGES = 20


def init_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Cache Wikipedia pages')
    parser.add_argument('-p', '--page', type=str, default='Erdős_number',
                        help='Starting Wikipedia page (default: Erdős_number)')
    parser.add_argument('-d', '--depth', type=int, default=3,
                        help='Depth of Wikipedia graph (default: 3)')
    return parser.parse_args()


def build_graph(start_page, depth) -> nx.DiGraph:
    visited: Set[str] = set()
    graph = nx.DiGraph()
    # для обхода графа в ширину (BFS)
    queue: List[Tuple[str, int]] = [(start_page, 0)]
    pages_cr: int = 0

    while queue and pages_cr < MAX_PAGES:
        page, level = queue.pop(0)
        if level >= depth:
            continue
        if page not in visited:
            pages_cr += page_ctrl(graph, queue, visited, page, level, pages_cr)

    return graph


def page_ctrl(graph, queue, visited, page, level, cr) -> int:
    info_page = f"{COLOR_GREEN} Посещение страницы №{cr}: {page}."
    info_level = f"Глубина графа: {level}{COLOR_RESET}"
    logging.info(info_page + info_level)
    visited.add(page)
    links = get_links_from_page("https://en.wikipedia.org/wiki/" + page)
    for link in links:
        if link not in visited:
            link = urllib.parse.unquote(link[6:]).replace('_', ' ')
            graph.add_edge(page, link)
            queue.append((link, level + 1))
            logging.info(f"Посещение страницы: {link}. Глубина графа: {level}")
            cr += 1
    return cr


def get_links_from_page(url: str) -> List[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()  # проверка на успешный запрос
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе к странице {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and ':' not in href and href != url:
            links.append(href)
    return links


def save_graph_to_json(graph, filename) -> None:
    data = {}
    for node in graph.nodes:
        clean_node = node
        data[clean_node] = list(graph.successors(node))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_graph_to_neo4j(graph, neo4j_driver) -> None:
    try:
        with neo4j_driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logging.info("База данных очищена")

            for node in graph.nodes:
                session.run("CREATE (a:Page {name: $name})", name=node)
            logging.info("Узлы созданы")

            for source, target in graph.edges:
                session.run(
                    "MATCH (a:Page {name: $source}), (b:Page {name: $target}) "
                    "CREATE (a)-[:LINKS_TO]->(b)",
                    source=source, target=target)
            logging.info("Ребра созданы")

    except AuthError as e:
        logging.error(f"Ошибка аутентификации: {e}")
    except ServiceUnavailable as e:
        logging.error(f"Служба недоступна: {e}")
    except ClientError as e:
        logging.error(f"Ошибка клиента: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


def get_neo4j_password() -> str:
    try:
        return os.environ['NEO4J_PASS']
    except KeyError:
        raise ValueError("Переменная окружения NEO4J_PASS не установлена")


if __name__ == "__main__":
    args = init_parse()
    depth = args.depth
    start_page = args.page

    logging.info(f"Начальная страница: {start_page}")
    logging.info(f"Глубина: {depth}")

    graph = build_graph(start_page, depth)

    if len(graph.nodes) < MIN_PAGES:
        start_page = 'Wikipedia:Very_short_featured_articles'
        info_wrn = f'Выбирается стартовая страница по умолчанию: {start_page}'
        logging.warning(f"Граф содержит менее {MIN_PAGES} страниц." + info_wrn)
        graph = build_graph("/wiki/" + start_page, depth)

    save_graph_to_json(graph, JSON_FILENAME)
    logging.info(f"{COLOR_GREEN}Граф записан в {JSON_FILENAME}{COLOR_RESET}")

    try:
        uri = "bolt://localhost:7687"
        username = 'neo4j'
        password = get_neo4j_password()
        neo4j_driver = GraphDatabase.driver(uri, auth=(username, password))
        neo4j_driver.verify_connectivity()
        logging.info("Подключение успешно установлено")

        save_graph_to_neo4j(graph, neo4j_driver)

    except AuthError as e:
        logging.error(f"Ошибка аутентификации: {e}")
    except ServiceUnavailable as e:
        logging.error(f"Служба Neo4j недоступна: {e}")
    except ClientError as e:
        logging.error(f"Ошибка клиента: {e}")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    finally:
        if 'neo4j_driver' in locals():
            neo4j_driver.close()
            logging.info("Соединение с Neo4j закрыто")
