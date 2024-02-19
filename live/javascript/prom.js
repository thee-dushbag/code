function sleep(delay = 0, callback = () => {}, ...args) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(callback(...args));
    }, delay * 1000);
  });
}

function getUrl(url = null) {
  return sleep(2, () => {
    return { status: 200, text: "Hello World", url };
  });
}

await sleep(3, (x, y) => x + y, 60, 40).then((value) =>
  console.log(`Result: ${value}`)
);

class Range {
  constructor(start, stop, step = 1) {
    this.start = start;
    this.stop = stop;
    this.step = step;
  }
}

Range.prototype[Symbol.asyncIterator] = async function* () {
  while (this.start < this.stop) {
    yield sleep(1, () => this.start);
    this.start += this.step;
  }
};

let urls = ["/greet", "/say_hi", "/home", "/index", "/lib"];

await Promise.all(
  urls.map((url) =>
    getUrl(url).then((value) => {
      console.log(`Received: '${value.text}' from '${value.url}'`);
      return value;
    })
  )
).then((results) => console.log(...results));

function* count(start = 1, step = 1) {
  while (true) {
    yield start;
    start += step;
  }
}

let gen = count();

for (let i = 0; i < 1000; i++) console.log(gen.next());

for await (let value of new Range(1, 11)) console.log(`Value: ${value}`);
