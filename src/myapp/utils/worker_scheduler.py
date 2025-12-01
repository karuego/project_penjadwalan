from PySide6.QtCore import QObject, Signal, QThread

# Import struct dan logika
# from .struct_jadwal import Jadwal # Tidak perlu import ini lagi disini
from . import sa as v6

class OptimizationWorker(QObject):
    # Ubah signal type hint jika perlu, tapi 'list' sudah cukup generic
    finished: Signal = Signal(list, float) 
    progress: Signal = Signal(int, float)
    error: Signal = Signal(str)

    def __init__(self, max_iter: int = 5000):
        super().__init__()
        self.max_iter: int = max_iter
        self._is_running: bool = True

    def run(self):
        """Fungsi ini akan berjalan di Thread terpisah"""
        try:
            def on_progress(iteration: int, current_cost: float):
                if self._is_running:
                    self.progress.emit(iteration, current_cost)

            # Jalankan Algoritma
            raw_schedule, final_cost = v6.simulated_annealing(
                max_iter=self.max_iter, progress_callback=on_progress
            )

            # --- PERUBAHAN DISINI ---
            # JANGAN convert ke QObject (Jadwal) di background thread!
            # Kirim raw_schedule (list of ScheduleItem dataclass) langsung ke Main Thread.
            
            self.finished.emit(raw_schedule, final_cost)

        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        self._is_running = False
