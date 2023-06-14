import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { StoreProvider } from './stateManagement/store';
import SocketService from './socketService';
import Router from './router';
import "./style.scss";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <StoreProvider>
    <Router />
    <SocketService />
  </StoreProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals

