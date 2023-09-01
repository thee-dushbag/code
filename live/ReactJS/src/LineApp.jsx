// import { ColorList, AddColorForm } from "./ColorList";
import { ColorProvider } from "./Context";
import {
  useState,
  useEffect,
  useContext,
  createContext,
  useLayoutEffect,
  useReducer,
  memo,
  useCallback, useRef, useMemo
} from "react";
export { App };


function CheckBox({ init = false }) {
  const [checked, setChecked] = useState(init);
  alert(`[NORMARL FLOW]: checked: ${checked.toString()}`);
  useEffect(() => alert(`[USE EFFECT]: checked: ${checked.toString()}`));
  return (
    <>
      <input
        type="checkbox"
        value={checked}
        onChange={() => setChecked((checked) => !checked)}
      />
      {checked ? "checked" : "not checked"}
    </>
  );
}

function Phrase({ init_value = "", init_phrase = "Example Phrase" }) {
  const [name, setName] = useState("Simon Nganga");
  const [value, setValue] = useState(init_value);
  const [phrase, setPhrase] = useState(init_phrase);
  const createPhrase = () => {
    setPhrase(value);
    setValue(init_value);
  };
  useEffect(() => {
    (async () => {
      await fetch(`http://127.0.0.1:5052/hello?name=${name}`, { method: "GET" })
        .then((resp) => resp.json())
        .then(
          (data) => setName(data.result),
          (error) => setName(error.toString())
        );
    })();
  }, []);
  useEffect(() => console.log(`typing: '${value}'`), [value]);
  useEffect(() => console.log(`saved phrase: '${phrase}'`), [phrase]);

  return (
    <>
      <h1>{name}</h1>
      <label htmlFor="phrase-input">Favorite Phrase: </label>
      <input
        type="text"
        value={value}
        placeholder={phrase}
        onChange={(e) => setValue(e.target.value)}
      />
      <button onClick={createPhrase}>Send</button>
    </>
  );
}

function useAnyKeyToRender() {
  const [key, setKey] = useState(""),
    eventKey = (e) => {
      setKey(e.key);
      console.log(`Key Set To: '${e.key}'`);
    },
    setUP = () => {
      console.log("Setup Function.");
      window.addEventListener("keydown", eventKey);
    },
    tearDOWN = () => {
      window.removeEventListener("keydown", eventKey);
      console.log("Teardown Function.");
    };
  useEffect(() => {
    setUP();
    return tearDOWN;
  }, [key]);
  return key;
}

function SetupTeardown() {
  const target = useRef();
  useEffect(() => {
    console.log("Target Loaded...");
    return () => console.log("Target Destroyed...");
  }, []);
  return (
    <div
      ref={target}
      onClick={() => target.current.remove()}
      id="target"
      className="bg-danger border m-2 border-2 border-primary rounded"
      style={{ height: "100px", width: "100px" }}
    ></div>
  );
}

function App() {
  return (
    <ColorProvider>
    </ColorProvider>
  );
}


const _Ctx = createContext();

function AppContext({ children }) {
  const [name, setName] = useState("");
  return <_Ctx.Provider value={{ name, setName }}>{children}</_Ctx.Provider>;
}

const useApp = () => useContext(_Ctx);

function NameForm() {
  const { setName } = useApp();
  const nameInput = useRef();
  const getName = (e) => {
    console.log("Changing Name");
    e.preventDefault();
    setName(nameInput.current.value);
    nameInput.current.value = "";
  };
  return (
    <form action="#" className="w-100">
      <input type="text" ref={nameInput} required placeholder="Name" />
      <input type="submit" value="Greet" onClick={getName} />
    </form>
  );
}

function HelloArea() {
  const { name } = useApp();
  const [greeting, setGreeting] = useState("");
  useMemo(() => {
    (async () => {
      console.log("Get Greeting for ", name);
      await fetch(`http://192.168.0.100:5052/greet?name=${name}`, {
        method: "GET",
      })
        .then((resp) => resp.json())
        .then((json) => setGreeting(json.greeting))
        .catch((error) => setGreeting(`Error Greeting ${name}: '${error}'`));
    })();
  }, [name])
  return <h1>{greeting}</h1>;
}

function Hooks() {
  useEffect(() => console.log("useEffect"));
  useLayoutEffect(() => console.log("useLayoutEffect"));
  return <div>Rendered</div>;
}

function IncrementReducer() {
  const [incBy, setIncBy] = useState(1);
  const [value, increment] = useReducer((v, inc) => v + inc, 0);
  return (
    <>
      <input
        type="number"
        placeholder="Increment By"
        value={incBy}
        onChange={(e) => setIncBy(Number.parseInt(e.target.value) || 1)}
      />
      <div onClick={() => increment(incBy)} className="btn btn-primary">
        Value: {value}
      </div>
    </>
  );
}

function Cat({ name, meow = (_) => _ }) {
  console.log(`rendering: ${name}`);
  return <p onClick={() => meow(name)}>{name}</p>;
}

const PureCat = memo(Cat);

function Cats() {
  const meow = useCallback((name) => console.log(`${name} cat is Meowing...`));
  const [names, addName] = useReducer(
    (names, name) => [...names, name],
    ["Biscuit", "Jungle", "Outlaw"]
  );
  return (
    <div>
      <h1>Cats</h1>
      <div className="cats">
        {names.map((name, index) => (
          <PureCat name={name} key={index} meow={meow} />
        ))}
      </div>
      <button
        onClick={() => addName(prompt("Name"))}
        className="btn btn-primary"
      >
        Add Cat
      </button>
    </div>
  );
}

function App() {
  return (
    <AppContext>
      {/* <Cats /> */}
      {/* <Hooks /> */}
      <HelloArea />
      <NameForm />
    </AppContext>
  );
}

export { App };
