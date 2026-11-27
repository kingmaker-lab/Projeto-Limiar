import assert from 'node:assert/strict';
import {Summary} from './summary.mjs';

const summary = new Summary();
for (let index = 0; index < 19; index++) summary.add({service:'api', status:200, ms:12});
summary.add({service:'api', status:503, ms:900});
summary.add({service:'auth', status:401, ms:5});
assert.deepEqual(summary.report(), [
  {service:'api', requests:20, errors:1, p95_upper_ms:25},
  {service:'auth', requests:1, errors:0, p95_upper_ms:5}
]);
assert.throws(() => summary.add({service:'api', status:999, ms:0}));
assert.throws(() => summary.add({service:'api', status:200, ms:NaN}));
