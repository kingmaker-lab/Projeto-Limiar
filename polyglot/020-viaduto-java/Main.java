import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws Exception {
        try {
            if (args.length != 2) throw new IllegalArgumentException("usage: Main SOURCE DESTINATION");
            Network graph = new Network();
            var input = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
            String line;
            int edges = 0;
            while ((line = input.readLine()) != null) {
                if (line.isBlank()) continue;
                var fields = line.strip().split("\\s+");
                if (fields.length != 3 || ++edges > 200000)
                    throw new IllegalArgumentException("expected FROM TO COST, up to 200000 edges");
                graph.add(fields[0], fields[1], Long.parseLong(fields[2]));
            }
            var route = graph.shortest(args[0], args[1]);
            if (route.isEmpty()) {
                System.out.println("unreachable");
                System.exit(1);
            }
            var value = route.orElseThrow();
            System.out.println("cost=" + value.cost());
            System.out.println(String.join(" -> ", value.path()));
        } catch (IllegalArgumentException error) {
            System.err.println(error.getMessage());
            System.exit(2);
        }
    }
}
