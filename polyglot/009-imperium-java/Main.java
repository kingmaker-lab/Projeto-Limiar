import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public final class Main {
    public static void main(String[] args) throws Exception {
        Inventory inventory = new Inventory();
        var input = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        String line;
        while ((line = input.readLine()) != null) {
            if (line.isBlank()) continue;
            String[] fields = line.strip().split("\\s+");
            try {
                switch (fields[0]) {
                    case "receive" -> {
                        if (fields.length != 4) throw new IllegalArgumentException("receive WH SKU QTY");
                        inventory.receive(fields[1], fields[2], Integer.parseInt(fields[3]));
                    }
                    case "transfer" -> {
                        if (fields.length != 5) throw new IllegalArgumentException("transfer FROM TO SKU QTY");
                        inventory.transfer(fields[1], fields[2], fields[3], Integer.parseInt(fields[4]));
                    }
                    case "report" -> {
                        if (fields.length != 1) throw new IllegalArgumentException("report takes no arguments");
                        System.out.println(inventory.report());
                    }
                    default -> throw new IllegalArgumentException("unknown command");
                }
            } catch (IllegalArgumentException | ArithmeticException error) {
                System.err.println(error.getMessage());
                System.exit(1);
            }
        }
    }
}
