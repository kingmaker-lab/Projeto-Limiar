export interface Component { id: string; label: string }
export interface Link { from: string; to: string }
export interface Graph { components: Component[]; links: Link[] }
export interface Positioned extends Component { x: number; y: number }

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw Error("Objeto inválido");
  return value as Record<string, unknown>;
}

export function parseGraph(input: unknown): Graph {
  const {components, links} = record(input);
  if (!Array.isArray(components) || !Array.isArray(links) ||
      components.length < 1 || components.length > 100 || links.length > 400)
    throw Error("Use de 1 a 100 componentes e até 400 conexões");
  const ids = new Set<string>();
  const nodes = components.map((value: unknown) => {
    const {id, label} = record(value);
    if (typeof id !== "string" || !/^[a-zA-Z0-9_-]{1,32}$/.test(id) || ids.has(id) ||
        typeof label !== "string" || !label.trim() || label.length > 40)
      throw Error("Componente inválido ou duplicado");
    ids.add(id);
    return {id, label};
  });
  const edges = new Set<string>();
  return {components: nodes, links: links.map((value: unknown) => {
    const {from, to} = record(value);
    if (typeof from !== "string" || typeof to !== "string" || from === to ||
        !ids.has(from) || !ids.has(to) || edges.has(from + ":" + to))
      throw Error("Conexão inválida ou duplicada");
    edges.add(from + ":" + to);
    return {from, to};
  })};
}

export function layout(graph: Graph): Positioned[] {
  const columns = Math.min(4, graph.components.length);
  return graph.components.map((component, index) => ({
    ...component, x: 125 + (index % columns) * 240, y: 70 + Math.floor(index / columns) * 130
  }));
}
