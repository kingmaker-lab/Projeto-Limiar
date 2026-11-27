require 'json'
require_relative 'ledger'

begin
  puts JSON.pretty_generate(Ledger.reconcile($stdin))
rescue ArgumentError, CSV::MalformedCSVError => error
  warn error.message
  exit 2
end
