from heapq import heapify, heappush


class FoodRateCuisine:
    def __init__(self, food: str, cuisine: str, rating: int):
        self.cuisine = cuisine
        self.rating = rating
        self.food = food

    def __eq__(self, frc: "FoodRateCuisine") -> bool:
        return (
            frc.rating == self.rating
            and frc.food == frc.food
            and frc.cuisine == self.cuisine
        )

    def __lt__(self, frc: "FoodRateCuisine") -> bool:
        if self.rating == frc.rating:
            return self.food < frc.food
        return self.rating > frc.rating

    def __str__(self) -> str:
        return dict(
            food=self.food,
            rating=self.rating,
            cuisine=self.cuisine,
        ).__str__()

    __repr__ = __str__


class FoodRatings:
    def __init__(self, foods: list[str], cuisines: list[str], ratings: list[int]):
        self.foodmap: dict[str, FoodRateCuisine] = {}
        self.cuisinemap: dict[str, list[FoodRateCuisine]] = {}
        for food, rating, cuisine in zip(foods, ratings, cuisines):
            state = FoodRateCuisine(food, cuisine, rating)
            self.foodmap[food] = state
            temp = self.cuisinemap.get(cuisine, [])
            heappush(temp, state)
            self.cuisinemap[cuisine] = temp

    def changeRating(self, food: str, newRating: int) -> None:
        target = self.foodmap[food]
        target.rating = newRating
        # NOTE: heapification is O(N) and redoing it after every
        # rate change is extremely expensive
        heapify(self.cuisinemap[target.cuisine]) # <- Very expensive
        # TODO: Make a simple sifter based on the index of a node
        # that hosds the value.

    def highestRated(self, cuisine: str) -> str:
        return self.cuisinemap[cuisine][0].food
