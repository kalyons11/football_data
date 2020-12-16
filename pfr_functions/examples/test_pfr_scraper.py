from pfr_functions.pfr_scraper import PFRScraper


if __name__ == '__main__':
    url = 'https://www.pro-football-reference.com/boxscores/201909220sfo.htm'
    all_tables = PFRScraper.find_tables(url)
    print('all tables')
    print(all_tables)

    for t in all_tables:
        print(t)
        try:
            d = PFRScraper.pull_table(url, t, header=True)
            print(d.columns)
        except IndexError:
            try:
                d = PFRScraper.pull_table(url, t, header=False)
                print(d.iloc[0])
            except:
                print(f'cannot load id {t}')

        print()


