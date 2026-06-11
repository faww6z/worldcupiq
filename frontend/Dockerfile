FROM node:24-slim

WORKDIR /app/frontend

COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npm", "run", "dev"]
