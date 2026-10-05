# Development image for the Vite dev server. Production serves the static build instead (Week 7).
FROM node:24.21.0-slim

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173
