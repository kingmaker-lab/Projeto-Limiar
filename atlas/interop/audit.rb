require 'base64'
require 'digest'
require 'json'
require 'net/http'
require 'openssl'

VERSION = 'ATLAS_GENESIS_V1'.freeze
ADDRESS = /\Aatl_[a-f0-9]{64}\z/
DIGEST = /\A[a-f0-9]{64}\z/

def check(condition, message)
  raise message unless condition
end

def digest(fields)
  Digest::SHA256.hexdigest(JSON.generate(fields))
end

def verify_transfer(tx, network, accounts)
  from, to, amount, nonce, pub, sig = tx.values_at('from', 'to', 'amount', 'nonce', 'publicKey', 'signature')
  check(ADDRESS.match?(from) && ADDRESS.match?(to) && from != to &&
    amount.is_a?(Integer) && amount.positive?, 'transferência inválida')
  sender = accounts[from]
  check(nonce.is_a?(Integer) && nonce == sender[:nonce] + 1, 'nonce incorreto')
  check(amount <= sender[:balance], 'saldo insuficiente')
  der = Base64.strict_decode64(pub)
  raw = Base64.strict_decode64(sig)
  check(der.bytesize == 91 && raw.bytesize == 64, 'chave ou assinatura inválida')
  key = OpenSSL::PKey.read(der)
  check(key.is_a?(OpenSSL::PKey::EC) && key.group.curve_name == 'prime256v1' &&
    key.public_to_der == der && 'atl_' + Digest::SHA256.hexdigest(der) == from, 'chave pública inválida')
  integers = raw.unpack('a32a32').map { |bytes| OpenSSL::ASN1::Integer.new(OpenSSL::BN.new(bytes, 2)) }
  signature = OpenSSL::ASN1::Sequence.new(integers).to_der
  payload = JSON.generate([VERSION + '/transfer', network, from, to, amount, nonce])
  check(key.verify('SHA256', signature, payload), 'assinatura inválida')
  sender[:nonce] += 1
  sender[:balance] -= amount
  accounts[to][:balance] += amount
end

def audit(ledger)
  actual, network, blocks = ledger.values_at('version', 'network', 'blocks')
  check(actual == VERSION && DIGEST.match?(network) && blocks.is_a?(Array) && blocks.size <= 4096, 'ledger inválido')
  accounts = Hash.new { |map, key| map[key] = { balance: 0, nonce: 0 } }
  tip = digest([VERSION + '/genesis', network])
  blocks.each_with_index do |block, index|
    height, previous, miner, tx, nonce, hash = block.values_at('height', 'previous', 'miner', 'transfer', 'nonce', 'hash')
    check(height.is_a?(Integer) && height == index + 1 && previous == tip && ADDRESS.match?(miner) &&
      nonce.is_a?(Integer) && nonce.between?(0, 499_999), 'cabeçalho inválido')
    transfer = tx&.values_at('from', 'to', 'amount', 'nonce', 'publicKey', 'signature')
    tip = digest([VERSION + '/block', network, height, previous, miner, transfer, nonce])
    check(tip.start_with?('00') && tip == hash, 'prova de trabalho inválida')
    verify_transfer(tx, network, accounts) unless tx.nil?
    accounts[miner][:balance] += 50
  end
  { network: network, height: blocks.size, tip: tip, supply: blocks.size * 50, accounts: accounts }
end

mode, source = ARGV
data = case mode
       when 'file'
         File.read(source)
       when 'peer'
         check(/\A[0-9]{1,5}\z/.match?(source), 'porta inválida')
         http = Net::HTTP.new('127.0.0.1', Integer(source, 10), nil)
         http.open_timeout = 2
         http.read_timeout = 10
         response = http.get('/v1/ledger')
         check(response.is_a?(Net::HTTPOK), 'HTTP ' + response.code)
         response.body
       else
         raise 'uso: ruby audit.rb file ARQUIVO | peer PORTA'
       end
puts JSON.generate(audit(JSON.parse(data)))
