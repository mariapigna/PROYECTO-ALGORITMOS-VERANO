class Pelicula:
    def __init__(self,title, episode_id, opening_crawl, director, release_date):
        self.title=title
        self.episode_id=episode_id
        self.opening_crawl=opening_crawl
        self.director=director
        self.realease_date=release_date

    def show_pelicula(self):
        print(f'''TITULO: {self.title}
    - Episodio: {self.episode_id}
    - Fecha de lanzamiento: {self.realease_date}
    - Director: {self.director}
    - Opening crawl:

{self.opening_crawl}''')