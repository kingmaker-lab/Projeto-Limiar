import { pathToFileURL } from 'node:url';
import { createHash, createPublicKey, verify } from 'node:crypto';
import { readFileSync } from 'node:fs';

const version = 'ATLAS_GENESIS_V1';
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const digest = (fields) => hash(JSON.stringify(fields));
const id = (value) => typeof value === 'string' && value.length === 64 && !/[^a-f0-9]/.test(value);
const address = (value) => typeof value === 'string' && value.startsWith('atl_') && id(value.slice(4));

function requireValid(condition, message) {
  if (!condition) throw new Error(message);
}

function decode(text, size) {
  const bytes = Buffer.from(text, 'base64');
  requireValid(bytes.length === size && bytes.toString('base64') === text, 'base64 inválido');
  return bytes;
}

export function blockHash(network, block) {
  const tx = block.transfer;
  const transfer = tx === null ? null : [tx.from, tx.to, tx.amount, tx.nonce, tx.publicKey, tx.signature];
  return digest([version + '/block', network, block.height, block.previous, block.miner, transfer, block.nonce]);
}

export function audit({ version: actual, network, blocks }) {
  requireValid(actual === version && id(network) && Array.isArray(blocks) && blocks.length <= 4096, 'ledger inválido');
  const accounts = {};
  const account = (key) => accounts[key] ??= { balance: 0, nonce: 0 };
  let tip = digest([version + '/genesis', network]);
  for (const [index, block] of blocks.entries()) {
    requireValid(block.height === index + 1 && block.previous === tip && address(block.miner)
      && Number.isSafeInteger(block.nonce) && block.nonce >= 0 && block.nonce < 500000, 'cabeçalho inválido');
    tip = blockHash(network, block);
    requireValid(tip.startsWith('00') && tip === block.hash, 'prova de trabalho inválida');
    const tx = block.transfer;
    if (tx !== null) {
      requireValid(address(tx.from) && address(tx.to) && tx.from !== tx.to
        && Number.isSafeInteger(tx.amount) && tx.amount > 0, 'transferência inválida');
      const from = account(tx.from);
      requireValid(tx.nonce === from.nonce + 1, 'nonce incorreto');
      requireValid(tx.amount <= from.balance, 'saldo insuficiente');
      const publicKey = decode(tx.publicKey, 91);
      const signature = decode(tx.signature, 64);
      const key = createPublicKey({ key: publicKey, format: 'der', type: 'spki' });
      requireValid(key.asymmetricKeyDetails?.namedCurve === 'prime256v1'
        && key.export({ format: 'der', type: 'spki' }).equals(publicKey)
        && 'atl_' + hash(publicKey) === tx.from, 'chave pública inválida');
      const payload = JSON.stringify([version + '/transfer', network, tx.from, tx.to, tx.amount, tx.nonce]);
      requireValid(verify('sha256', Buffer.from(payload), { key, dsaEncoding: 'ieee-p1363' }, signature), 'assinatura inválida');
      from.balance -= tx.amount;
      from.nonce++;
      account(tx.to).balance += tx.amount;
    }
    account(block.miner).balance += 50;
  }
  return { network, height: blocks.length, tip, supply: blocks.length * 50, accounts };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [mode, source] = process.argv.slice(2);
  if (mode === 'file') {
    console.log(JSON.stringify(audit(JSON.parse(readFileSync(source, 'utf8')))));
  } else if (mode === 'peer' && /^[0-9]{1,5}$/.test(source)) {
    const response = await fetch('http://127.0.0.1:' + source + '/v1/ledger', {
      redirect: 'error', signal: AbortSignal.timeout(10000),
    });
    requireValid(response.ok, 'HTTP ' + response.status);
    console.log(JSON.stringify(audit(await response.json())));
  } else {
    throw new Error('uso: node audit.mjs file ARQUIVO | peer PORTA');
  }
}
