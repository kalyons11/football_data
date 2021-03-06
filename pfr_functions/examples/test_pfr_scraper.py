from pfr_functions.pfr_scraper import PFRScraper


if __name__ == '__main__':
    url = 'https://www.pro-football-reference.com/boxscores/201909220sfo.htm'
    all_tables = PFRScraper.find_tables(url)
    print('all tables')
    print(all_tables)

    for t in all_tables:
        try:
            d = PFRScraper.pull_table(url, t)
            # TODO need to add post-processing so columns is
            # always valid
            # right now, if header is not parsed correctly, then columns
            # will have a bunch of None values and be useless
            print(f'{t}: {d.columns}')
            print()
        except Exception as e:
            print(e)


