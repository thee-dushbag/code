// // function App() {
// //   const [colors, setColors] = useState(colorData);
// //   const deleteColor = (cid) =>
// //     setColors(colors.filter((color) => color.id !== cid));
// //   const rateColor = (cid, rating) =>
// //     setColors(
// //       colors.map((color) => (color.id === cid ? { ...color, rating } : color))
// //     );
// //   const addColor = (title, color) =>
// //     setColors([...colors, { title, color, rating: 0, id: v4() }]);
// //   return (
// //     <>
// //       <AddColorForm onNewColor={addColor} />
// //       <ColorList
// //         onRateColor={rateColor}
// //         colors={colors}
// //         onRemoveColor={deleteColor}
// //       />
// //     </>
// //   );
// // }

// // function StarRating({ totalStars = 5, rating = 1, style = {}, ...props }) {
// //   const [rate, setRating] = useState(rating);
// //   return (
// //     <div style={{ padding: "5px", ...style }} {...props}>
// //       {createArray(totalStars).map((_, i) => (
// //         <Star
// //           key={i}
// //           onSelect={(_) => setRating(i + 1)}
// //           selected={rate > i}
// //         />
// //       ))}
// //       <p>
// //         {rate} of {totalStars} stars.
// //       </p>
// //     </div>
// //   );
// // }


// // function ColorList({
// //   colors = [],
// //   onRemoveColor = (f) => f,
// //   onRateColor = (f) => f,
// // }) {
// //   if (!colors.length) return <div>No Colors Listed.</div>;
// //   return (
// //     <div>
// //       {colors.map((color) => (
// //         <Color
// //           {...color}
// //           onRate={onRateColor}
// //           key={color.id}
// //           onRemove={onRemoveColor}
// //         />
// //       ))}
// //     </div>
// //   );
// // }

// // function AddColorForm({ onNewColor = (f) => f }) {
// //   const txtTitle = useRef();
// //   const hexColor = useRef();
// //   const onSubmit = (event) => {
// //     event.preventDefault();
// //     onNewColor(txtTitle.current.value, hexColor.current.value);
// //     txtTitle.current.value = "";
// //     hexColor.current.value = "";
// //   };
// //   return (
// //     <form action="#" onSubmit={onSubmit}>
// //       <input type="text" ref={txtTitle} required placeholder="Color Title" />
// //       <input type="color" ref={hexColor} required />
// //       <input type="submit" value="Add Color" />
// //     </form>
// //   );
// // }

// // function AddColorForm({ onNewColor = (f) => f }) {
// //   const DEFAULT_COLOR = "#000000";
// //   const [title, setTitle] = useState("");
// //   const [color, setColor] = useState(DEFAULT_COLOR);
// //   const onSubmit = (event) => {
// //     event.preventDefault();
// //     onNewColor(title, color);
// //     setTitle("");
// //     setColor(DEFAULT_COLOR);
// //   };
// //   return (
// //     <form action="#" onSubmit={onSubmit}>
// //       <input
// //         type="text"
// //         onChange={(event) => setTitle(event.target.value)}
// //         required
// //         placeholder="Color Title"
// //       />
// //       <br />
// //       <label htmlFor="">Color</label>
// //       <input
// //         type="color"
// //         onChange={(event) => setColor(event.target.value)}
// //         required
// //       />
// //       <br />
// //       <input type="submit" value="Add Color" />
// //     </form>
// //   );
// // }

// import { FaRecycle, FaArrowCircleDown } from "react-icons/fa";
// import { DataHook, useInput } from "./hooks";
// export { App }; // Hoisting

// function Spinner({ children }) {
//   return <div className="rotate-anime">{children}</div>;
// }

// function Loading({ dataKey }) {
//   // return (
//   //   <>
//   //     <MoonLoader color="white" /> Fetching '{dataKey}' from server ...
//   //   </>
//   // );
//   return (
//     <Spinner>
//       <FaArrowCircleDown className="spinner" /> Fetching '{dataKey}' from
//       server...{" "}
//     </Spinner>
//   );
// }

// function GetData({ dataKey }) {
//   return (
//     <DataHook
//       url={`http://127.0.0.1:5052/data?key=${dataKey}`}
//       onData={(data) => <pre>{JSON.stringify(data, null, 2)}</pre>}
//       onError={(error, reload) => (
//         <pre>
//           An Error occurred loading {dataKey}
//           <button
//             className="btn btn-primary btn-small float-end me-3"
//             onClick={reload}
//           >
//             <FaRecycle />
//           </button>
//         </pre>
//       )}
//       onLoad={() => <Loading dataKey={dataKey} />}
//     />
//   );
// }


// function Error({ error, reload = (_) => _ }) {
//   return (
//     <div className="p-4 bg-danger text-light">
//       <button className="float-end btn-primary btn" onClick={reload}>
//         <FaRecycle />
//       </button>
//       {error}
//     </div>
//   );
// }

// function LiveLoad() {
//   const urlTemplate = "http://localhost:5052/data?key=$key";
//   const [key, keyReset] = useInput("");
//   const [url, setUrl] = useReducer((_, newKey) =>
//     urlTemplate.replace("$key", newKey)
//   );
//   let [cKey, setCKey] = useReducer((_, lkey) => lkey.value, key.value);
//   const onFetch = (e) => {
//     if (!key.value) return;
//     setUrl(key.value);
//     setCKey(key);
//     keyReset();
//   };
//   return (
//     <div>
//       <div className="d-flex">
//         <input
//           className="flex-fill"
//           type="text"
//           {...key}
//           placeholder="Enter Key to Fetch."
//         />
//         <button className="flex-shrink btn btn-primary mx-2" onClick={onFetch}>
//           Fetch
//         </button>
//       </div>
//       <DataHook
//         url={url}
//         onLoad={() => <Loading dataKey={cKey} />}
//         onData={(data, reload) => <Person {...data} reload={reload} />}
//         onError={(error, reload) => <Error error={error} reload={reload} />}
//       />
//     </div>
//   );
// }