from urllib.parse import urlparse


def get_parent_link(url):
    parsed_url = urlparse(url)
    parent_link = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_url)
    return parent_link
