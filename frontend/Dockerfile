# # # build env
# FROM node:14-alpine as build
# WORKDIR /app
# COPY frontend .
# RUN npm install
# RUN npm run build
# # CMD cp -r build result_build


# build env
# FROM node:14-alpine as build
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . ./
# RUN npm run build
# CMD cp -r build result_build

FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
CMD cp -r build result_build