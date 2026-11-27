require 'stringio'
require_relative 'ledger'

def run(rows)
  Ledger.reconcile(StringIO.new(Ledger::HEADER.join(',') + "\n" + rows))
end

report = run("t,cash,125,0\nt,sales,0,125\nu,cash,0,25\nu,refunds,25,0\n")
raise report.inspect unless report == {transactions: 2, balances_cents: {'cash'=>100,'refunds'=>25,'sales'=>-125}}
["a,cash,10,0\nb,sales,0,10\n", "a,cash,10,10\n", ""].each do |invalid|
  begin
    run(invalid)
    raise "accepted invalid ledger"
  rescue ArgumentError
  end
end
