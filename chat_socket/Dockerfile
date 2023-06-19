FROM node

WORKDIR /chat_socket
COPY . .

RUN npm install --quiet
RUN npm install --global nodemon
CMD nodemon index.js