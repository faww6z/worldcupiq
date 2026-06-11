FROM node:24-slim AS deps

WORKDIR /app/frontend

COPY package*.json ./
RUN npm ci

FROM deps AS dev
COPY . .
CMD ["npm", "run", "dev"]

FROM deps AS build
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
