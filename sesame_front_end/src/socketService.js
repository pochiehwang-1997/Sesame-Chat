import React, { useState, useEffect, useContext } from "react";
import openSocket from "socket.io-client";
import { store } from "./stateManagement/store";
import { activeChatAction } from "./stateManagement/actions";

const SOCKET_URL = "http://chats-LoadB-1XE49U9OIKCDD-f806f98acf2c8594.elb.us-east-1.amazonaws.com:9000";
let socket;

const SocketService = () => {
  const {
    state: { userDetail, activeChatUser },
    dispatch,
  } = useContext(store);
  const [canTurnOffSocket, setCanTurnOffSocket] = useState(false);

  useEffect(() => {
    // Remove all listeners before create one listener
    if (canTurnOffSocket) {
      socket.removeAllListeners("command");
    } else {
      setCanTurnOffSocket(true);
      socket = openSocket(SOCKET_URL);
    }
    socket.on("command", (data) => {
      if (!userDetail || !activeChatUser) return;
      if (userDetail.id !== data.receiver.id) return;
      if (activeChatUser.id !== data.sender.id) return;
      dispatch({ type: activeChatAction, payload: data });
    });
  }, [userDetail, activeChatUser]);
  return <></>;
};

export default SocketService;
