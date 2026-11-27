package limiar.pulse

import org.junit.Assert.assertTrue
import org.junit.Test

class DiagnosticsTest {
    @Test fun formatsMissingBatteryAndLowMemory() {
        val lines = Snapshot(35, 4, 0, 1024L * 1024, 0, 10, null, true).lines()
        assertTrue(lines.any { "indisponível" in it })
        assertTrue(lines.any { "pouca memória" in it })
        assertTrue(lines.any { "0 de 1 MiB" in it })
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejectsInvalidBattery() { Snapshot(35, 4, 0, 10, 0, 10, 101, false) }
}
