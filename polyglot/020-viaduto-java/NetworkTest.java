import java.util.List;

public class NetworkTest {
    public static void main(String[] args) {
        var graph = new Network();
        graph.add("A", "B", 9);
        graph.add("A", "C", 2);
        graph.add("C", "B", 3);
        graph.add("B", "C", 0);
        var route = graph.shortest("A", "B").orElseThrow();
        assert route.cost() == 5 && route.path().equals(List.of("A", "C", "B"));
        assert graph.shortest("B", "A").isEmpty();
        assert graph.shortest("A", "A").orElseThrow().cost() == 0;
        try { graph.add("X", "Y", -1); throw new AssertionError("accepted negative cost"); }
        catch (IllegalArgumentException expected) { assert graph.shortest("A", "B").orElseThrow().equals(route); }
    }
}
