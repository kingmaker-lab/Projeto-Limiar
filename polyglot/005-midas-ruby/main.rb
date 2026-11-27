require 'json'
require_relative 'invoice'

begin
  abort 'usage: ruby main.rb standard|partner FILE.csv' unless ARGV.size == 2
  puts JSON.pretty_generate(Invoice.calculate(CSV.read(ARGV[1]), ARGV[0]))
rescue ArgumentError, CSV::MalformedCSVError, SystemCallError => error
  abort error.message
end
