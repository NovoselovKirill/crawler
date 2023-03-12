from argparse import ArgumentParser, Namespace


def _check_if_place_to_save_set(parser: ArgumentParser, args: Namespace):
    if args.zip or args.folder:
        return
    parser.error('No place to save set. Add --folder or --zip')


def parse() -> Namespace:
    parser = ArgumentParser(description='Crawler')

    parser.add_argument('start_url', help='starting URL')
    parser.add_argument('-d', '--domains', nargs='*', help='allowed domains')
    parser.add_argument('-f', '--file', help='file containing allowed domains')
    parser.add_argument('-m', '--max_depth', type=int, help='maximum depth of crawling')
    parser.add_argument('-z', '--zip', help='path to save results as a zip archive')
    parser.add_argument('-o', '--folder', help='path to save results as a folder')
    parser.add_argument('-t', '--num_threads', type=int, default=-1, help='number of threads to use')
    parser.add_argument('-i', '--ignore_robots', action='store_true', help='ignore robots.txt file and crawl all pages')

    namespace = parser.parse_args()
    _check_if_place_to_save_set(parser, namespace)

    return namespace


print(parse())