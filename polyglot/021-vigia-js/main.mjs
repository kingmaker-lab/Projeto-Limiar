import {createInterface} from 'node:readline';
import {Summary} from './summary.mjs';

const summary = new Summary();
let lineNumber = 0;
try {
  for await (const line of createInterface({input: process.stdin, crlfDelay: Infinity})) {
    lineNumber++;
    if (!line.trim()) continue;
    if (line.length > 4096) throw Error("line exceeds 4096 characters");
    summary.add(JSON.parse(line));
  }
  console.log(JSON.stringify(summary.report(), null, 2));
} catch (error) {
  console.error(`line ${lineNumber}: ${error.message}`);
  process.exitCode = 2;
}
