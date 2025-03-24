using System;
using System.IO;
using System.Text.Json;

namespace Minitwit.Web.Helpers;

public class GCLogger
{
    public static void LogGarbageCollection(string action)
    {
        try
        {
            var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            var gcInfo = GC.GetGCMemoryInfo();

            var logEntry = new
            {
                date = timestamp,
                action,
                totalAvailableMemory = gcInfo.TotalAvailableMemoryBytes,
                highMemoryLoadThreshold = gcInfo.HighMemoryLoadThresholdBytes,
                memoryLoad = gcInfo.MemoryLoadBytes,
                heapSize = gcInfo.HeapSizeBytes,
                fragmentedBytes = gcInfo.FragmentedBytes,
                lastGcGeneration = gcInfo.Generation,
                gen0Collections = GC.CollectionCount(0),
                gen1Collections = GC.CollectionCount(1),
                gen2Collections = GC.CollectionCount(2)
            };

            string logFilePath = "gc_debug.log";
            string logJson = JsonSerializer.Serialize(logEntry) + Environment.NewLine;

            string combinedPath = Path.Combine("..", logFilePath);

            // Fully qualify System.IO.File to avoid conflicts
            if (!File.Exists(combinedPath))
            {
                File.Create(combinedPath);
            }
            ;
            File.AppendAllText(combinedPath, logJson);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error logging garbage collection: {ex.Message}");
        }
    }
}
