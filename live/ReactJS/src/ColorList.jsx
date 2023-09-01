import { StarRating } from "./StarRating";
import { FaTrash } from "react-icons/fa";
import { useInput } from "./hooks";
import { useColors } from "./Context";
export { ColorList, AddColorForm };

function AddColorForm() {
  const [titleProps, resetTitle] = useInput("");
  const [colorProps, resetColor] = useInput("#000000");
  const { addColor } = useColors();

  const onSubmit = (event) => {
    event.preventDefault();
    addColor(titleProps.value, colorProps.value);
    resetTitle();
    resetColor();
  };
  return (
    <form action="#" onSubmit={onSubmit}>
      <input type="text" {...titleProps} required placeholder="Color Title" />
      <br />
      <label htmlFor="">Color</label>
      <input type="color" {...colorProps} required />
      <br />
      <input type="submit" value="Add Color" />
    </form>
  );
}

function Color({ id, rating, title, color }) {
  const { deleteColor, rateColor } = useColors();
  return (
    <section>
      <h1>
        <FaTrash height={"15pt"} onClick={(_) => deleteColor(id)} color="red" />{" "}
        {title}
      </h1>
      <div style={{ height: 50, backgroundColor: color }} />
      <StarRating onRate={(rating) => rateColor(id, rating)} rating={rating} />
    </section>
  );
}

function ColorList() {
  const { colors } = useColors();
  if (!colors.length) return <div>No Colors Listed.</div>;
  return (
    <div>
      {colors.map((color) => (
        <Color {...color} key={color.id} />
      ))}
    </div>
  );
}
