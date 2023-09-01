export { Main };

export default Main;

let sleep = (delay) =>
  new Promise((resolve) => setTimeout(resolve, delay * 1000));

await sleep(10)

function Main() {
  return <div className="main">This is the main component.</div>;
}
