import {createServer} from "node:http";
import {readFile} from "node:fs/promises";

const routes = new Map([
  ["/", ["index.html", "text/html; charset=utf-8"]],
  ["/dist/app.js", ["dist/app.js", "text/javascript"]],
  ["/dist/model.js", ["dist/model.js", "text/javascript"]],
]);
createServer(async (request, response) => {
  const route = routes.get(request.url);
  if (request.method !== "GET" || !route) {
    response.writeHead(404).end();
    return;
  }
  try {
    const body = await readFile(new URL(route[0], import.meta.url));
    response.writeHead(200, {"Content-Type": route[1]}).end(body);
  } catch {
    response.writeHead(500).end("Execute npm run build.");
  }
}).listen(8080, "127.0.0.1", () => console.log("http://127.0.0.1:8080"));
