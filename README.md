## Ports & Endpoints (local testing)

All services run on localhost (127.0.0.1).

- Gateway (price + news server) — `127.0.0.1:9000`  
  - Streams messages (delimiter `*`) to connected clients.

- OrderBook — client connecting to Gateway at `127.0.0.1:9000`  
  - Parses ticks and updates shared memory.

- OrderManager (order receiver) — `127.0.0.1:9001`  
  - Receives order JSON messages from Strategy (delimiter `*`).

- Strategy — connects to:
  - Gateway: `127.0.0.1:9000`
  - OrderManager: `127.0.0.1:9001`
