from .database import Database as Database
from .database_manager import DatabaseManager as DatabaseManager

from .hari import Hari as Hari
from .struct_waktu import TimeSlot as TimeSlot
from .waktu_util import (
    TimeSlotValidator as TimeSlotValidator,
    TimeSlotManager as TimeSlotManager,
)

from .struct_pengajar import Pengajar as Pengajar
from .struct_matakuliah import MataKuliah as MataKuliah
from .struct_ruangan import Ruangan as Ruangan

from .schedule_generator import ScheduleGenerator as ScheduleGenerator
# from .struktur import (
#     # Ruangan as Ruangan,
#     Dosen as Dosen,
#     # MataKuliah as MataKuliah,
#     Waktu as Waktu,
#     Pengampu as Pengampu,
#     PreferensiDosen as PreferensiDosen,
#     JadwalItem as JadwalItem,
# )
