FROM node:23-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install --no-cache

COPY . .
RUN npm run build

FROM nginx:stable-alpine

# Copy the self-signed certificate
COPY certs/cert.pem /etc/ssl/certs/backend-cert.pem

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built frontend files
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

