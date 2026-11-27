import {layout, parseGraph} from "./model.js";

const form = document.querySelector("form")!;
const textarea = document.querySelector("textarea")!;
const canvas = document.querySelector("canvas")!;
const status = document.querySelector<HTMLElement>("#status")!;
const connections = document.querySelector("ul")!;
const context = canvas.getContext("2d")!;

function render() {
  try {
    const graph = parseGraph(JSON.parse(textarea.value));
    const nodes = layout(graph);
    const byId = new Map(nodes.map(node => [node.id, node]));
    canvas.width = Math.max(...nodes.map(node => node.x)) + 125;
    canvas.height = Math.max(...nodes.map(node => node.y)) + 70;
    connections.replaceChildren();
    context.strokeStyle = context.fillStyle = "#536978";
    context.lineWidth = 2;
    for (const {from, to} of graph.links) {
      const source = byId.get(from)!;
      const target = byId.get(to)!;
      const angle = Math.atan2(target.y - source.y, target.x - source.x);
      const dx = Math.cos(angle), dy = Math.sin(angle);
      const distance = Math.min(92 / Math.abs(dx), 22 / Math.abs(dy));
      const x = target.x - dx * distance, y = target.y - dy * distance;
      context.beginPath();
      context.moveTo(source.x, source.y);
      context.lineTo(x, y);
      context.lineTo(x - 12 * Math.cos(angle - .4), y - 12 * Math.sin(angle - .4));
      context.moveTo(x, y);
      context.lineTo(x - 12 * Math.cos(angle + .4), y - 12 * Math.sin(angle + .4));
      context.stroke();
      const item = document.createElement("li");
      item.textContent = source.label + " → " + target.label;
      connections.append(item);
    }
    context.font = "15px system-ui";
    context.textAlign = "center";
    context.textBaseline = "middle";
    for (const node of nodes) {
      context.fillStyle = "#173648";
      context.fillRect(node.x - 92, node.y - 22, 184, 44);
      context.fillStyle = "#fff";
      context.fillText(node.label, node.x, node.y, 172);
    }
    status.textContent = graph.components.length + " componentes · " + graph.links.length + " conexões";
  } catch (error) {
    canvas.width = 0;
    canvas.height = 0;
    connections.replaceChildren();
    status.textContent = String(error);
  }
}
form.addEventListener("submit", event => { event.preventDefault(); render(); });
render();
