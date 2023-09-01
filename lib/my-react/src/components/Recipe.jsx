import { Ingredients, Steps } from "./Ingredients";

function Recipe({ name, ingredients, steps }) {
  return (
    <section>
      <h1 className="recipe-header">
        <u>{name}</u>
      </h1>
      <Ingredients ingredients={ingredients} />
      <Steps steps={steps} />
    </section>
  );
}

export { Recipe };
