this.onmessage = (event) => {
  console.log(`Received: ${event.data} from web.js`);
  this.postMessage(event.data * event.data);
};
