import data from "./data/recipes.json" assert { type: "json" };
import React from "react";
import ReactDOM from "react-dom/client";
import { Menu } from "./components/Menu";

const { recipes } = data;

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Menu recipes={recipes} />);
