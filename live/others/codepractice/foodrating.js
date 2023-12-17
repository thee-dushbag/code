class FoodRatings {
  constructor(foods, cuisines, ratings) {
    this.foodmap = new Map();
    this.cuisinemap = new Map();
    let ratestate, temp;
    for (let index = 0; index < foods.length; index++) {
      ratestate = {
        food: foods[index],
        cuisine: cuisines[index],
        rating: ratings[index],
      };
      this.foodmap.set(ratestate.food, ratestate);
      temp = this.cuisinemap.get(ratestate.cuisine) || [];
      temp.push(ratestate);
      this.cuisinemap.set(ratestate.cuisine, temp);
    }
  }

  changeRating(food, newRating) {
    this.foodmap.get(food).rating = newRating;
  }

  highestRated(cuisine) {
    let targets = this.cuisinemap
      .get(cuisine)
      .slice()
      .sort((item1, item2) => item2.rating - item1.rating);
    return targets
      .filter((item) => item.rating === targets[0].rating)
      .sort((item1, item2) => item1.food.localeCompare(item2.food))[0].food;
  }
}
