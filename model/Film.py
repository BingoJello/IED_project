class Film:
    def __init__(self, id, rd, n, pb, dg, wg, d, g):
        self.id = id
        self.release_date = rd
        self.name = n
        self.production_budget = pb
        self.domestic_gross = dg
        self.worldwide_gross = wg
        self.distributor = d
        self.genre = g
        self.directors = []
        self.producers = []
        self.actors = []

    def get_id(self) :
        return self.id

    def set_id(self, id) :
        self.id = id

    def get_release_date(self) :
        return self.release_date

    def set_release_date(self, release_date) :
        self.release_date = release_date

    def get_name(self) :
        return self.name

    def set_name(self, name) :
        self.name = name

    def get_production_budget(self) :
        return self.production_budget

    def set_production_budget(self, production_budget) :
        self.production_budget = production_budget

    def get_domestic_gross(self) :
        return self.domestic_gross

    def set_domestic_gross(self, domestic_gross) :
        self.domestic_gross = domestic_gross

    def get_worldwide_gross(self) :
        return self.worldwide_gross

    def set_worldwide_gross(self, worldwide_gross) :
        self.worldwide_gross = worldwide_gross

    def get_distributor(self) :
        return self.distributor

    def set_distributor(self, distributor) :
        self.distributor = distributor

    def get_genre(self) :
        return self.genre

    def set_genre(self, genre) :
        self.genre = genre

    def get_directors(self) :
        return self.directors

    def set_directors(self, directors) :
        self.directors = directors

    def get_actors(self) :
        return self.actors

    def set_actors(self, actors) :
        self.actors = actors

    def get_producers(self) :
        return self.producers

    def set_producers(self, producers) :
        self.producers = producers