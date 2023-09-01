import "./App.css";
import { useState, useRef } from "react";

function Line({ line, lineId, lineDeleter }) {
  return (
    <div
      className="text-light user-select-none lead p-2 rounded border border-success text-wrap w-100"
      onDoubleClick={(e) => lineDeleter(lineId)}
    >
      {line}
    </div>
  );
}

function LineForm({ addline }) {
  const inputRef = useRef();
  function _addLine(event) {
    event.preventDefault();
    let currentLine = inputRef.current.value;
    if (currentLine.length > 0) {
      addline(currentLine);
      inputRef.current.value = "";
      inputRef.current.focus();
    }
  }
  return (
    <div className="p-2 rounded gap-3 border border-danger d-flex">
      <input
        className="flex-fill font-monospace px-2 py-1 rounded"
        type="text"
        name="line"
        placeholder="Enter Line."
        id="line_id"
        ref={inputRef}
      />
      <input
        type="button"
        className="flex-shrink btn btn-danger"
        value="Add Line"
        onClick={_addLine}
      />
    </div>
  );
}

function Lines({ lines, lineDeleter }) {
  return (
    <div className="border rounded flex-fill border-warning gap-2 p-2 d-flex flex-column">
      {lines.length > 0 ? (
        lines.map((line, index) => (
          <Line
            key={index}
            line={line}
            lineId={index}
            lineDeleter={lineDeleter}
          />
        ))
      ) : (
        <Line
          key={0}
          lineId={-1}
          line={"No Lines to show..."}
          lineDeleter={lineDeleter}
        />
      )}
    </div>
  );
}

function LineAppHeader({ text }) {
  return (
    <div className="border rounded p-2">
      <h1 className="m-0 font-comic-shanns-mono text-center">
        <u>{text}</u>
      </h1>
    </div>
  );
}

function LineAppFooter({ text }) {
  return (
    <div className="text-opacity-25 p-2 border rounded text-end">
      {text}
    </div>
  );
}

function LineApp() {
  const [lines, addLine] = useState([]);
  const deleteLine = (lineIndex) =>
    addLine(lines.filter((_, index) => index !== lineIndex));
  return (
    <div className="w-100 h-100 border text-light p-1 bg-dark gap-2 d-flex flex-column">
      <LineAppHeader text={"Line Application"} />
      <LineForm addline={(line) => addLine([...lines, line])} />
      <Lines lines={lines} lineDeleter={deleteLine} />
      <LineAppFooter text={"made by react."} />
    </div>
  );
}

function LineAppPage() {
  return (
    <div className="container vh-100 vw-100 g-0">
      <div className="row d-flex h-100 g-0 w-100 justify-content-center align-items-center">
        <div className="col-xl-7 g-0 h-100 col-lg-9 col-md-11 col-sm-12 col-xs-12">
          <LineApp />
        </div>
      </div>
    </div>
  );
}

export default LineApp

export {
  LineAppHeader,
  LineForm,
  Lines,
  Line,
  LineAppFooter,
  LineApp,
  LineAppPage,
};