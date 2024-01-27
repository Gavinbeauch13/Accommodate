class StarCounter:
    def __init__(self):
        self.fullstars = 0
        self.halfstar = 0
        self.emptystars = 0

    def count_stars(self, stars):
        for i in range(5):
            if stars >= 1:
                self.fullstars += 1
                stars -= 1
            elif stars >= 0.5:
                self.halfstar += 1
                stars -= 0.5
            elif stars == 0:
                self.emptystars += 1

    def get_counts(self):
        return {
            "Full Stars": self.fullstars,
            "Half Star": self.halfstar,
            "Empty Stars": self.emptystars
        }