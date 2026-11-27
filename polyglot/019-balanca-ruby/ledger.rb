require 'csv'

module Ledger
  HEADER = %w[transaction account debit_cents credit_cents].freeze
  ID = /\A[a-zA-Z0-9_-]{1,48}\z/

  def self.reconcile(input)
    csv = CSV.new(input)
    raise ArgumentError, "invalid header" unless csv.shift == HEADER

    balances = Hash.new(0)
    transactions = Hash.new { |index, key| index[key] = [0, 0] }
    csv.each do |row|
      transaction, account, debit, credit = row
      unless row.size == 4 && transaction&.match?(ID) && account&.match?(ID) &&
             [debit, credit].all? { |value| value&.match?(/\A[0-9]{1,12}\z/) }
        raise ArgumentError, "invalid row #{csv.lineno}"
      end
      debit, credit = debit.to_i, credit.to_i
      raise ArgumentError, "expected one positive side, row #{csv.lineno}" unless debit.positive? ^ credit.positive?

      totals = transactions[transaction]
      totals[0] += debit - credit
      totals[1] += 1
      balances[account] += debit - credit
    end
    raise ArgumentError, "empty ledger" if transactions.empty?

    invalid = transactions.select { |_id, (net, count)| !net.zero? || count < 2 }.keys.sort
    raise ArgumentError, "unbalanced transactions: #{invalid.join(', ')}" unless invalid.empty?

    {transactions: transactions.size, balances_cents: balances.sort.to_h}
  end
end
