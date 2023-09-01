import { FaStar } from "react-icons/fa";

function Star({ selected = false, onSelect = (f) => f }) {
  return <FaStar onClick={onSelect} color={selected ? "red" : "grey"} />;
}

function createArray(length) {
  return [...Array(length)];
}

function StarRating({ totalStars = 5, rating = 1, style = {}, onRate = f => f }) {
  return (
    <span>
      {createArray(totalStars).map((_, i) => (
        <Star
          key={i}
          onSelect={_ => onRate(i + 1)}
          selected={rating > i}
        />
      ))}
      <p>
        {rating} of {totalStars} stars.
      </p>
    </span>
  );
}

export { Star, StarRating, createArray };
