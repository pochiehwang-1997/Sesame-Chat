import React, { createContext, useReducer } from "react";
import { updateChatReducer, updateChatState } from "./reducers";

const reduceReducer =
  (...reducers) =>
  (prevState, value, ...args) => {
    reducers.reduce(
      (newState, reducer) => reducer(newState, value, ...args),
      prevState
    );
  };

const combineReducers = reduceReducer(updateChatReducer);
const initialState = {...updateChatState};

const store = createContext(initialState);
const { Provider } = store;

const StoreProvider = ({ children }) => {
  const [state, dispatch] = useReducer(combineReducers, initialState);

  return <Provider value={{ state, dispatch }}>{children}</Provider>;
};

export { store, StoreProvider };
