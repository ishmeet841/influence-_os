
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f package-lock.json ]; then npm ci; elif [ -f yarn.lock ]; then yarn; else npm i; fi
COPY . .
EXPOSE 3000
CMD [ "npm", "run", "dev" ]
