import { Axios } from "axios";
import "./App.css";
import { useRef } from "react";

let ax = new Axios({ baseURL: "http://192.168.0.100:5052" });

function Hello({ message }) {
  return <h1 className="text-center font-comicshanns">{message}</h1>;
}

// function MessageBox() {
//   let msgInput = useRef();
//   async function sendMessage(event) {
//     console.log("Sending");
//     let message = msgInput.current.value;
//     msgInput.current.value = "";
//     if (message.length > 0) {
//       await fetch("http://192.168.0.100:5052/msg", {
//         body: JSON.stringify({ message }),
//         method: "POST",
//       }).then(async (resp) => {
//         let smsg = await resp.json();
//         alert(`Server Said: "${smsg.message}"`);
//       });
//     }
//   }
//   return (
//     <div
//       className="p-2 border rounded d-flex flex-column gap-2 w-100"
//       style={{ height: "6cm" }}
//     >
//       <div className="flex-shrink text-center h1">
//         <u>Fetch API</u>
//       </div>
//       <textarea
//         name="message"
//         ref={msgInput}
//         id="msgInput"
//         className="w-100 p-2 bg-transparent text-light font-comicshanns flex-fill rounded"
//       ></textarea>
//       <div onClick={sendMessage} className="btn flex-shrink btn-primary w-100">
//         Send
//       </div>
//     </div>
//   );
// }

function MessageBoxAxios() {
  let msgInput = useRef();
  async function sendMessage(event) {
    console.log("Sending");
    let message = msgInput.current.value;
    if (message.length > 0) {
      msgInput.current.value = "";
      await ax.post("/msg", JSON.stringify({ message })).then(async (resp) => {
        let msg;
        if (resp.status === 200) {
          let smsg = JSON.parse(resp.data);
          msg = `Server Said: "${smsg.message}"`;
        } else msg = `Error Occurred:[${resp.status}]: "${resp.statusText}"`;
        alert(msg);
      });
    }
  }
  return (
    <div
      className="p-2 border font-comicshanns rounded d-flex flex-column gap-2 w-100"
      style={{ height: "6cm" }}
    >
      <div className="flex-shrink text-center h1">
        <u>Axios API</u>
      </div>
      <textarea
        name="message"
        ref={msgInput}
        id="msgInput"
        className="w-100 p-2 bg-transparent text-light flex-fill rounded"
      ></textarea>
      <div onClick={sendMessage} className="btn flex-shrink btn-primary w-100">
        Send
      </div>
    </div>
  );
}

function LearnPage() {
  return (
    <div className="container vh-100 vw-100">
      <div className="row d-flex align-items-center justify-content-center">
        <div className="col-xl-6 col-lg-7 col-md-10 col-sm-12 col-xs-12">
          <Hello message={"Hello World"} />
          <MessageBoxAxios />
        </div>
      </div>
    </div>
  );
}

export default LearnPage;

export { Hello };
