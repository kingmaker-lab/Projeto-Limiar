import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

public final class Inventory {
    private final Map<String, Map<String, Integer>> warehouses = new HashMap<>();

    public void receive(String location, String sku, int quantity) {
        validate(location, sku, quantity);
        int balance = Math.addExact(balance(location, sku), quantity);
        warehouses.computeIfAbsent(location, key -> new HashMap<>()).put(sku, balance);
    }

    public void transfer(String from, String to, String sku, int quantity) {
        validate(from, sku, quantity);
        validate(to, sku, quantity);
        if (from.equals(to)) throw new IllegalArgumentException("same warehouse");
        int available = balance(from, sku);
        if (available < quantity) throw new IllegalArgumentException("insufficient stock");
        receive(to, sku, quantity);
        if (available == quantity) warehouses.get(from).remove(sku);
        else warehouses.get(from).put(sku, available - quantity);
    }

    public int balance(String location, String sku) {
        return warehouses.getOrDefault(location, Map.of()).getOrDefault(sku, 0);
    }

    public String report() {
        var result = new TreeMap<String, Map<String, Integer>>();
        warehouses.forEach((location, stock) -> {
            if (!stock.isEmpty()) result.put(location, new TreeMap<>(stock));
        });
        return result.toString();
    }

    private static void validate(String location, String sku, int quantity) {
        if (!location.matches("[A-Z0-9_-]{1,32}") || !sku.matches("[A-Z0-9_-]{1,32}") || quantity <= 0)
            throw new IllegalArgumentException("invalid warehouse, SKU or quantity");
    }
}
