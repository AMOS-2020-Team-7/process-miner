# build Angular app
FROM node:current-alpine AS node-build
ARG BACKEND_HOST
ARG BACKEND_PORT
ENV BACKEND_HOST ${BACKEND_HOST}
ENV BACKEND_PORT ${BACKEND_PORT}
WORKDIR /usr/src/app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN sh script/set_backend_access_data.sh
RUN node_modules/@angular/cli/bin/ng build --prod

# serve Angular app
FROM nginx:alpine
COPY --from=node-build /usr/src/app/dist/psd2miner-frontend /usr/share/nginx/html
COPY nginx-angular.conf /etc/nginx/conf.d/default.conf
