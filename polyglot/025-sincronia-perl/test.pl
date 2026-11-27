use strict;
use warnings;
use FindBin;
use lib $FindBin::Bin;
use Test::More tests => 4;
use Timeline qw(retime);

sub transform {
    my ($data, @settings) = @_;
    open my $in, '<', \$data or die $!;
    open my $out, '>', \my $output or die $!;
    retime($in, $out, @settings);
    close $out or die $!;
    return $output;
}
my $sample = "1\r\n00:00:01,000 --> 00:00:05,000\r\nFirst\r\nSecond\r\n";
is(transform($sample, 100, 1, 2), "1\n00:00:00,600 --> 00:00:02,600\nFirst\nSecond\n");
eval { transform($sample, -2000, 1, 1) };
like($@, qr/outside/);
eval { transform("1\n00:00:01,000 --> 00:00:01,001\nx\n", 0, 1, 100) };
like($@, qr/collapsed/);
eval { transform("1\n00:00:01,000 --> 00:00:02,000\n", 0, 1, 1) };
like($@, qr/subtitle text/);
