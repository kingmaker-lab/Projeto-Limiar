require 'csv'

module Invoice
  def self.calculate(rows, tier)
    discount_rate = {'standard' => 0, 'partner' => 10}.fetch(tier) do
      raise ArgumentError, 'tier must be standard or partner'
    end
    raise ArgumentError, 'empty invoice' if rows.empty?

    subtotal = rows.sum do |row|
      sku, quantity, cents = row
      unless row.size == 3 && sku&.match?(/\A[A-Z0-9_-]{1,32}\z/) &&
             quantity&.match?(/\A[1-9][0-9]{0,5}\z/) && cents&.match?(/\A[0-9]{1,9}\z/)
        raise ArgumentError, 'expected SKU,positive quantity,unit price in cents'
      end
      quantity.to_i * cents.to_i
    end
    discount = (subtotal * discount_rate + 50) / 100
    tax = ((subtotal - discount) * 8 + 50) / 100
    {subtotal_cents: subtotal, discount_cents: discount,
     tax_cents: tax, total_cents: subtotal - discount + tax}
  end
end
