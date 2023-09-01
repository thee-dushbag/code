function Ingredient({ ingredient }) {
  return <li className="ingredient">{ingredient}</li>;
}
function Ingredients({ ingredients }) {
  return (
    <ol className="ingredients">
      {ingredients.map((ingredient, index) => (
        <Ingredient key={index} ingredient={ingredient} />
      ))}
    </ol>
  );
}

function Step({ step }) {
  return <li className="step">{step}</li>;
}

function Steps({ steps }) {
  return (
    <ol className="steps">
      {steps.map((step, index) => (
        <Step key={index} step={step} />
      ))}
    </ol>
  );
}

export { Steps, Ingredients };
