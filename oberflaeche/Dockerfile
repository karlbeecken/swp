FROM node:16.13.0-alpine3.14

# Create app directory
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY package.json /usr/src/app/
COPY yarn.lock /usr/src/app/
COPY . /usr/src/app/

# Install node modules
ONBUILD RUN yarn install

#RUN yarn build

ENV HOST 0.0.0.0

CMD [ "yarn", "dev"]