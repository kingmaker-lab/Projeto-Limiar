use strict;
use warnings;
use FindBin;
use lib $FindBin::Bin;
use Timeline qw(retime);

die "usage: perl main.pl OFFSET_MS [NUMERATOR DENOMINATOR]\n" unless @ARGV == 1 || @ARGV == 3;
my ($offset, $numerator, $denominator) = @ARGV;
binmode STDIN, ':raw';
binmode STDOUT, ':raw';
eval { retime(\*STDIN, \*STDOUT, $offset, $numerator // 1, $denominator // 1); 1 } or do {
    warn $@;
    exit 2;
};
close STDOUT or die "cannot close output: $!\n";
