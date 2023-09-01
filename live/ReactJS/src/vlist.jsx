import { useEffect } from "react";
import data from "./people.json";
import { FixedSizeList } from "react-window";
let { people } = data;
export { App };

function Person({ name, age, email, index, style }) {
  useEffect(() => {
    console.log(`[${index}]: Adding ${name}`);
    return () => console.log(`[${index}]: Removing ${name}`);
  }, []);
  if (!(name && age && email)) return null;
  return (
    <div
      style={{ ...style, overflow: "hidden", width: "95%" }}
      className="py-3 d-flex row-gap-3 px-3 rounded border border-primary m-2"
    >
      <img
        src={`http://192.168.0.100:9944/image?width=115&height=115&index=${index}`}
        alt={`Image for ${name.split(" ")[0]}`}
      />
      <div className="ps-3">
        <div>Index : {index}</div>
        <div>Name : {name}</div>
        <div>Email : {email}</div>
        <div>Age : {age}</div>
      </div>
    </div>
  );
}

function List({ data = [], forEach = (f) => f }) {
  return (
    <div>
      {data.map((item, index) => (
        <div key={index}>{forEach(item, index)}</div>
      ))}
    </div>
  );
}

function App() {
  console.log(people.length);
  return (
    <FixedSizeList
      height={window.innerHeight}
      width={window.innerWidth}
      itemCount={people.length}
      itemSize={150}
    >
      {({ index, style }) => (
        <Person {...people[index]} style={style} index={index} />
      )}
    </FixedSizeList>
  );
  // return <List data={people} forEach={Person} />;
}
