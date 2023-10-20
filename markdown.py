import sys
from recipe_scrapers import scrape_me

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Please provide web link')
        exit(0)

    link = sys.argv[1]
    try:
        scraper = scrape_me(link)
    except:
        scraper = scrape_me(link, wild_mode = True)

    f = None
    try:
        try:
            f = open(f'./recipes/{scraper.title()}.md', 'w')
        except:
            print(f'Could not open file {scraper.title()}.md. Writing to recipe.md')
            f = open('./recipes/recipe.md', 'w')

        f.write(f'**Total Time:** {scraper.total_time()}\n\n')
        f.write(f'**Servings:** {scraper.yields()}\n\n')
        f.write(f'**Source:** [{scraper.host()}]({link})\n\n')
        
        f.write('## Ingredients\n')
        for s in scraper.ingredients():
            s1 = s.split(' ', 1)
            if len(s1) == 1:
                f.write(f'{s1[0]}\n\n')
            else:
                f.write(f'**{s1[0]}** {s1[1]}\n\n')

        f.write('## Directions\n')
        for s in scraper.instructions_list():
            f.write(f'{s}\n\n')

    finally:
        if f is not None:
            f.close()
