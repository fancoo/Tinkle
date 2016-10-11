# -*- coding:utf-8 -*-


def get_page(url):
    """download source code of a page according
    to the url"""
    try:
        if url == "http://xkcd.com/353":
            return """Depending on the purpose of your site, choose a name that can be easily recognized and reflects the site’s theme.

                      Try not to have a domain name that sounds or spell out like your competitor. You do not want visitors to accidentally visit other than your site.

                      Vanity url is a trend now. For more options on vanity url, get yours from “iwantmyname” service provider.Use keywords related words in the domain name that describe your site (if it makes sense). The domain name should suggest the nature of your product or service. A good domain name describes exactly what the site is about. It is important for a visitor to get an idea of what the website is about just by looking at the domain name. For example, our site service is to make awareness to success in blogging so I take it "besuccessblogger".

                      Easy to Remeber

                      Your domain name should be easy to remember because your visitors will want to type in the domain name in the web browser for revisits and if they can’t remember the domain name then you loose a huge amount potential traffic. It is also easier to spread the word of mouth when the domain name is easy to remember.

                      Keep your domain name short"""
    except:
        return ""
    return ""


def get_next_target(html):
    """get url from a html, each time return one,
    we can constantly call this function until get all urls"""
    start_link = html.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = html.find('"', start_link)
    end_quote = html.find('"', start_quote + 1)
    url = html[start_quote+1:end_quote]
    return url, end_quote


def get_all_links(html):
    """get all links in a html"""
    links = []
    while True:
        url, endpos = get_next_target(html)
        if url:
            links.append(url)
            html = html[endpos:]
        else:
            break
    return links


def union(p, q):
    """merge p and q, store the no-duplicate item in p"""
    for i in q:
        if i not in p:
            p.append(i)


def lookup(index, keyword):
    """find all links for a keyword in index.

        index:[[keyword1, [url1, url2,...], [key2, [url3,...]"""
    for item in index:
        if item[0] == keyword:
            return item[1]
    return []


def add_to_index(index, keyword, url):
    """add a [keyword, [url..]] to an index"""
    for entry in index:
        if entry[0] == keyword:
            links = lookup(index, keyword)  # avoid duplicated
            if url not in links:
                entry[1].append(url)
                return
    index.append([keyword, [url]])


def add_page_to_index(index, url, content):
    """for every page, divide it's words and store the
    url for every word to make an index
    sample:
    >>add_page_to_index(index,'fake.text',"This is a test")
    >> [['This', ['fake.text']], ['is', ['fake.text']], ['a', ['fake.text']],
    >> ['test',['fake.text']]]"""
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
    return index


def crawl_web(seed):
    """automatically download html according to the
    "seed"(a primitive url), get all links, download more pages and
    loop till ends"""
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        url = tocrawl.pop()
        if url not in crawled:
            content = get_page(url)
            add_page_to_index(index, url, content)
            union(tocrawl, get_all_links(content))
    return index

seed = "http://xkcd.com/353"
index = crawl_web(seed)
print lookup(index, "name")





