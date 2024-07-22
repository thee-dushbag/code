let worker = new Worker("./worker.js");

worker.onmessage = (event) => {
  console.log(`Received ${event.data} from worker.js`);
};

worker.postMessage(90);
