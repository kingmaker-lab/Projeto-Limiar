import assert from 'node:assert/strict';
import { execFileSync, spawn } from 'node:child_process';
import { createPrivateKey, createPublicKey, sign } from 'node:crypto';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { once } from 'node:events';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { blockHash } from './audit.mjs';

const [, , binary] = process.argv;
assert(binary, 'uso: node interop/check.mjs CAMINHO_DO_BINÁRIO');
const work = mkdtempSync(join(tmpdir(), 'atlas-interop-'));
const ledgerDir = join(work, 'ledger');
const go = (...args) => execFileSync(binary, ['-dir', ledgerDir, ...args], { encoding: 'utf8' });
const clients = [
  ['JavaScript', process.execPath, fileURLToPath(new URL('audit.mjs', import.meta.url))],
  ['Ruby', 'ruby', fileURLToPath(new URL('audit.rb', import.meta.url))],
];

function mineFixture(network, block) {
  for (let nonce = 0; nonce < 500000; nonce++) {
    block.nonce = nonce;
    block.hash = blockHash(network, block);
    if (block.hash.startsWith('00')) return block;
  }
  throw new Error('limite de mineração da amostra');
}

let peer;
try {
  const aliceKey = join(work, 'alice.pem');
  const bobKey = join(work, 'bob.pem');
  const alice = go('wallet', aliceKey).trim();
  const bob = go('wallet', bobKey).trim();
  go('init');
  go('mine', alice);
  const transfer = join(work, 'transfer.json');
  writeFileSync(transfer, go('sign', aliceKey, bob, '17'));
  go('mine', alice, transfer);

  // In the other direction, Node signs an independent transfer that Go mines.
  const { network } = JSON.parse(go('status'));
  const key = createPrivateKey(readFileSync(bobKey));
  const payload = JSON.stringify(['ATLAS_GENESIS_V1/transfer', network, bob, alice, 5, 1]);
  writeFileSync(transfer, JSON.stringify({
    from: bob, to: alice, amount: 5, nonce: 1,
    publicKey: createPublicKey(key).export({ format: 'der', type: 'spki' }).toString('base64'),
    signature: sign('sha256', Buffer.from(payload), { key, dsaEncoding: 'ieee-p1363' }).toString('base64'),
  }));
  go('mine', alice, transfer);
  const expected = JSON.parse(go('status'));
  assert.equal(expected.height, 3);
  assert.equal(expected.supply, 150);
  assert.deepEqual(expected.accounts[alice], { balance: 138, nonce: 1 });
  assert.deepEqual(expected.accounts[bob], { balance: 12, nonce: 1 });

  peer = spawn(binary, ['-dir', ledgerDir, 'serve', '0'], { stdio: ['ignore', 'pipe', 'inherit'] });
  const lines = createInterface({ input: peer.stdout });
  const [listening] = await Promise.race([
    once(lines, 'line', { signal: AbortSignal.timeout(5000) }),
    once(peer, 'exit').then(([code]) => { throw new Error('servidor encerrou: ' + code); }),
  ]);
  const port = /^127\.0\.0\.1:(\d+)$/.exec(listening)?.[1];
  assert(port, 'endereço local inválido');

  // Re-mining the malformed blocks ensures their rejection is due to signature or nonce.
  const ledger = JSON.parse(readFileSync(join(ledgerDir, 'ledger.json')));
  const modified = structuredClone(ledger);
  modified.blocks.length = 2;
  modified.blocks[1].transfer.amount++;
  mineFixture(network, modified.blocks[1]);
  const replay = structuredClone(ledger);
  replay.blocks.push(mineFixture(network, {
    height: 4, previous: expected.tip, miner: alice, transfer: ledger.blocks[1].transfer,
  }));
  const badPow = structuredClone(ledger);
  badPow.blocks[0].hash = '0'.repeat(64);
  const invalid = [
    [modified, 'assinatura inválida'],
    [replay, 'nonce incorreto'],
    [badPow, 'prova de trabalho inválida'],
  ];

  const invalidDir = join(work, 'invalid');
  mkdirSync(invalidDir);
  for (const [sample, error] of invalid) {
    writeFileSync(join(invalidDir, 'ledger.json'), JSON.stringify(sample));
    assert.throws(
      () => execFileSync(binary, ['-dir', invalidDir, 'status'], { stdio: ['ignore', 'pipe', 'pipe'] }),
      (err) => err.status === 1 && err.stderr.includes(error),
    );
  }
  for (const [name, runtime, script] of clients) {
    const run = (...args) => execFileSync(runtime, [script, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    assert.deepEqual(JSON.parse(run('peer', port)), expected);
    for (const [sample, error] of invalid) {
      const file = join(work, 'invalid.json');
      writeFileSync(file, JSON.stringify(sample));
      assert.throws(() => run('file', file), (err) => err.status === 1 && err.stderr.includes(error));
    }
    console.log(name + ': estado idêntico ao Go via HTTP; assinatura, replay e PoW inválidos rejeitados');
  }
  console.log('Go aceitou assinatura criada em JavaScript. Altura 3, emissão 150, saldos 138 e 12.');
} finally {
  if (peer && peer.exitCode === null && peer.signalCode === null && peer.pid) {
    const closed = once(peer, 'close');
    peer.kill();
    await closed;
  }
  rmSync(work, { recursive: true, force: true });
}
