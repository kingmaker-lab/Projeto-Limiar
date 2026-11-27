import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.PriorityQueue;
import java.util.regex.Pattern;

final class Network {
    private static final Pattern NODE = Pattern.compile("[a-zA-Z0-9_-]{1,48}");
    record Edge(String destination, long cost) {}
    record Candidate(String node, long cost) {}
    record Route(long cost, List<String> path) {}
    private final Map<String, List<Edge>> edges = new HashMap<>();

    void add(String from, String to, long cost) {
        validate(from);
        validate(to);
        if (cost < 0 || cost > 1_000_000_000L) throw new IllegalArgumentException("invalid edge cost");
        edges.computeIfAbsent(from, ignored -> new ArrayList<>()).add(new Edge(to, cost));
        edges.computeIfAbsent(to, ignored -> new ArrayList<>());
    }

    Optional<Route> shortest(String source, String destination) {
        validate(source);
        validate(destination);
        if (!edges.containsKey(source) || !edges.containsKey(destination))
            throw new IllegalArgumentException("unknown endpoint");

        var distance = new HashMap<String, Long>();
        var previous = new HashMap<String, String>();
        var frontier = new PriorityQueue<>(Comparator.comparingLong(Candidate::cost).thenComparing(Candidate::node));
        frontier.add(new Candidate(source, 0));
        distance.put(source, 0L);
        while (!frontier.isEmpty()) {
            var current = frontier.remove();
            if (current.cost() != distance.get(current.node())) continue;
            if (current.node().equals(destination)) {
                var path = new ArrayList<String>();
                for (String node = destination; node != null; node = previous.get(node)) path.add(node);
                Collections.reverse(path);
                return Optional.of(new Route(current.cost(), List.copyOf(path)));
            }
            for (Edge edge : edges.get(current.node())) {
                long cost = current.cost() + edge.cost();
                if (cost >= distance.getOrDefault(edge.destination(), Long.MAX_VALUE)) continue;
                distance.put(edge.destination(), cost);
                previous.put(edge.destination(), current.node());
                frontier.add(new Candidate(edge.destination(), cost));
            }
        }
        return Optional.empty();
    }

    private static void validate(String node) {
        if (!NODE.matcher(node).matches()) throw new IllegalArgumentException("invalid node");
    }
}
