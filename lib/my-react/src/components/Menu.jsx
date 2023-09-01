import { Recipe } from "./Recipe";

function Menu({ recipes }) {
  return (
    <section className="recipe-menu">
      {recipes.map((recipe, index) => (
        <Recipe
          key={index}
          name={recipe.name}
          ingredients={recipe.ingredients}
          steps={recipe.steps}
        />
      ))}
    </section>
  );
}

export { Menu };
