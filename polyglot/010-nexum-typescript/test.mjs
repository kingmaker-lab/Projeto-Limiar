import assert from "node:assert/strict";
import {layout, parseGraph} from "./dist/model.js";

const graph = parseGraph({components: [{id:"a",label:"Site"}, {id:"b",label:"API"}],
  links: [{from:"a",to:"b"}, {from:"b",to:"a"}]});
assert.equal(layout(graph)[1].x, 365);
assert.equal(graph.links.length, 2);
assert.throws(() => parseGraph({...graph, components: [graph.components[0], graph.components[0]]}));
assert.throws(() => parseGraph({...graph, links: [{from:"a",to:"missing"}]}));
