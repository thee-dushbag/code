import { createContext, useContext, useState } from "react";
import { colorData } from "./colorData";
import { v4 } from "uuid";

const ColorsContext = createContext();

function ColorProvider({ children }) {
  const [colors, setColors] = useState(colorData);

  const deleteColor = (cid) =>
    setColors(colors.filter((color) => color.id !== cid));

  const rateColor = (cid, rating) =>
    setColors(
      colors.map((color) => (color.id === cid ? { ...color, rating } : color))
    );

  const addColor = (title, color) =>
    setColors([...colors, { title, color, rating: 0, id: v4() }]);

  return (
    <ColorsContext.Provider
      value={{ colors, deleteColor, addColor, rateColor }}
    >
      {children}
    </ColorsContext.Provider>
  );
}
const useColors = () => useContext(ColorsContext);

export { ColorProvider, useColors };
