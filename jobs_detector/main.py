import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    "Remote", "Postgres", "Python",
    "Javascript", "React", "Pandas"
]


@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    if keywords:
        keywords_list = keywords.split(',')
    else:
        keywords_list = DEFAULT_KEYWORDS

    url = 'https://news.ycombinator.com/item?id={}'.format(post_id)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        data = BeautifulSoup(r.text, 'html.parser')
        posts = data.find_all(class_='athing')  # ('tr',
        # job_postings = [post.text for post in posts if post.find("img", width="0") if post.find("span", class_ = "c00")]
        job_postings = []
        for post in posts:
            if post.find("img", width="0"):
                if post.find("span", class_="c00"):
                    job_postings.append(post.text)

    total_no_job_posts = len(job_postings)

    print("Total job posts: {}".format(total_no_job_posts))

    keyword_results = get_postings_matching_keywords(job_postings,
                                                     keywords_list)

    print ("Keywords:")
    print ("\n")
    for k, v in keyword_results.items():
        print("{}: {} ({}%)".format(k.title(), v,
                                    get_percentage(v, total_no_job_posts)))

    if combinations:
        combo_list = [combo.split('-') for combo in combinations]
        combinations_results = get_postings_matching_combinations(job_postings,
                                                                  combo_list)
        print("\n")
        print("Combinations:")
        for k, v in combinations_results.items():
            print(
            "{}: {} ({}%)".format(k, v, get_percentage(v, total_no_job_posts)))


def get_percentage(value, total):
    return int(float(value) / total * 100)


def get_postings_matching_keywords(postings, keywords):
    # if any of the keywords are in postings
    results = {key: sum([1 for post in postings if key.lower() in post])
               for key in keywords}

    return results


def get_postings_matching_combinations(postings, combinations):
    # results = {key: sum([1 for post in postings if key in post])
    # for key in combinations}
    # if all keywords are in postings

    results = {}
    for combo in combinations:
        results['-'.join(combo).title()] = 0

    for post in postings:
        for combo in combinations:
            if all([True if kw in post else False for kw in combo]):
                results['-'.join(combo).title()] += 1

    return results


if __name__ == '__main__':
    jobs_detector()