package limiar.pulse

import android.app.Activity
import android.app.ActivityManager
import android.os.BatteryManager
import android.os.Build
import android.os.Bundle
import android.os.StatFs
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            val inset = (24 * resources.displayMetrics.density).toInt()
            setPadding(inset, inset * 2, inset, inset * 2)
        }
        val report = TextView(this).apply { textSize = 17f }
        val refresh = Button(this).apply {
            text = "Atualizar diagnóstico"
            setOnClickListener { report.text = collect().lines().joinToString("\n\n") }
        }
        layout.addView(refresh)
        layout.addView(report)
        setContentView(ScrollView(this).apply { addView(layout) })
        refresh.performClick()
    }

    private fun collect(): Snapshot {
        val memory = ActivityManager.MemoryInfo()
        getSystemService(ActivityManager::class.java).getMemoryInfo(memory)
        val storage = StatFs(filesDir.absolutePath)
        val battery = getSystemService(BatteryManager::class.java)
            .getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY).takeIf { it in 0..100 }
        return Snapshot(Build.VERSION.SDK_INT, Runtime.getRuntime().availableProcessors(),
            memory.availMem, memory.totalMem, storage.availableBytes, storage.totalBytes,
            battery, memory.lowMemory)
    }
}
