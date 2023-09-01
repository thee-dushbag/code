const title = (sentence) =>
  sentence
    .split(" ")
    .map((word) => word[0].toUpperCase() + word.substr(1))
    .join(" ");

export { title };
