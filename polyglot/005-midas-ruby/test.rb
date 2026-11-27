require_relative 'invoice'

invoice = Invoice.calculate([%w[A 2 199], %w[B 1 102]], 'partner')
raise invoice.inspect unless invoice == {subtotal_cents: 500, discount_cents: 50,
                                         tax_cents: 36, total_cents: 486}
[[[], 'standard'], [[%w[A 0 100]], 'standard'], [[%w[A 1 2]], 'unknown']].each do |rows, tier|
  begin
    Invoice.calculate(rows, tier)
    raise 'invalid invoice accepted'
  rescue ArgumentError
  end
end
