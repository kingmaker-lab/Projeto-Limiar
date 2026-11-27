public final class InventoryTest {
    public static void main(String[] args) {
        Inventory inventory = new Inventory();
        inventory.receive("A", "PART", 10);
        inventory.transfer("A", "B", "PART", 3);
        assert inventory.balance("A", "PART") == 7 && inventory.balance("B", "PART") == 3;
        try {
            inventory.transfer("A", "B", "PART", 12);
            throw new AssertionError("accepted shortage");
        } catch (IllegalArgumentException expected) {
            assert inventory.balance("A", "PART") == 7;
        }
        inventory.receive("B", "BIG", Integer.MAX_VALUE);
        inventory.receive("A", "BIG", 1);
        try {
            inventory.transfer("A", "B", "BIG", 1);
            throw new AssertionError("accepted overflow");
        } catch (ArithmeticException expected) {
            assert inventory.balance("A", "BIG") == 1;
        }
    }
}
