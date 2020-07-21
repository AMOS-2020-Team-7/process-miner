# build Angular app
FROM node:current-alpine AS node-build
WORKDIR /usr/src/app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# serve Angular app
FROM nginx:alpine
COPY --from=node-build /usr/src/app/dist/psd2miner-frontend /usr/share/nginx/html
COPY nginx-angular.conf /etc/nginx/conf.d/default.conf
