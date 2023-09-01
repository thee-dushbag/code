// import { createGraphiQLFetcher } from '@graphiql/toolkit';
// import { GraphiQL } from 'graphiql';
// import 'graphiql/graphiql.css';
// import React from 'react';
// import { createRoot } from 'react-dom/client';

// const fetcher = createGraphiQLFetcher({ url: 'http://localhost:5052/graphql' });

// const root = createRoot(document.getElementById('root'));
// root.render(<GraphiQL fetcher={fetcher} />);

import ReactDOM from "react-dom/client";
import React from "react";
import "./App.css";
import { App } from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
