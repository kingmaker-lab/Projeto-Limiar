package Timeline;
use strict;
use warnings;
use Exporter 'import';
our @EXPORT_OK = qw(retime);

sub milliseconds {
    my ($value) = @_;
    $value =~ /\A([0-9]{2}):([0-5][0-9]):([0-5][0-9]),([0-9]{3})\z/
        or die "invalid timestamp\n";
    return (($1 * 60 + $2) * 60 + $3) * 1000 + $4;
}

sub render_time {
    my ($value) = @_;
    die "timestamp outside 00:00:00,000..99:59:59,999\n" if $value < 0 || $value >= 360_000_000;
    return sprintf '%02d:%02d:%02d,%03d',
        int($value / 3_600_000), int($value / 60_000) % 60, int($value / 1000) % 60, $value % 1000;
}

sub retime {
    my ($input, $output, $offset, $numerator, $denominator) = @_;
    die "offset must be integer milliseconds\n"
        unless defined $offset && $offset =~ /\A[+-]?[0-9]{1,9}\z/;
    for my $part ($numerator, $denominator) {
        die "expected positive ratio parts up to 100000\n"
            unless defined $part && $part =~ /\A[0-9]{1,6}\z/ && $part > 0 && $part <= 100000;
    }
    my $previous = 0;
    my $started = 0;
    my $needs_body = 0;
    while (my $line = <$input>) {
        $line =~ s/\r?\n\z//;
        if (!$started) {
            $line =~ s/\A\xEF\xBB\xBF// if $previous == 0;
            next if $line eq '';
            die "expected increasing subtitle index\n"
                unless $line =~ /\A[0-9]{1,9}\z/ && $line > $previous;
            $previous = $line;
            my $range = <$input> // die "missing time range\n";
            $range =~ s/\r?\n\z//;
            my ($first, $last) = split / --> /, $range, -1;
            die "invalid time range\n" unless defined $last && $range eq "$first --> $last";
            my $from = milliseconds($first);
            my $to = milliseconds($last);
            die "end must follow start\n" unless $to > $from;
            $from = int(($from * $numerator + int($denominator / 2)) / $denominator) + $offset;
            $to = int(($to * $numerator + int($denominator / 2)) / $denominator) + $offset;
            die "scaled interval collapsed\n" unless $to > $from;
            print {$output} "$line\n", render_time($from), " --> ", render_time($to), "\n"
                or die "cannot write output\n";
            $started = $needs_body = 1;
        } else {
            die "missing subtitle text\n" if $needs_body && $line eq '';
            $needs_body = 0;
            $started = 0 if $line eq '';
            print {$output} "$line\n" or die "cannot write output\n";
        }
    }
    die "expected subtitle text\n" if !$previous || $needs_body;
}

1;
