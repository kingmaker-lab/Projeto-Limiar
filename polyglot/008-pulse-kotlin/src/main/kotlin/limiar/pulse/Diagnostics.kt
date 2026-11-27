package limiar.pulse

data class Snapshot(
    val sdk: Int,
    val cores: Int,
    val availableMemory: Long,
    val totalMemory: Long,
    val availableStorage: Long,
    val totalStorage: Long,
    val batteryPercent: Int?,
    val lowMemory: Boolean
) {
    init {
        require(sdk > 0 && cores > 0)
        require(availableMemory in 0..totalMemory && availableStorage in 0..totalStorage)
        require(batteryPercent == null || batteryPercent in 0..100)
    }

    fun lines(): List<String> = listOf(
        "Android API $sdk · $cores núcleos lógicos",
        "RAM livre: ${availableMemory / MIB} de ${totalMemory / MIB} MiB",
        "Espaço livre: ${availableStorage / MIB} de ${totalStorage / MIB} MiB",
        "Bateria: ${batteryPercent?.let { "$it%" } ?: "indisponível"}",
        if (lowMemory) "O sistema sinaliza pouca memória." else "Memória dentro do limite do sistema."
    )

    companion object { private const val MIB = 1024L * 1024 }
}
