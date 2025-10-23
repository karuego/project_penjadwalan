from .database_manager import DatabaseManager
from .waktu_util import TimeSlotManager
from .schedule_generator import ScheduleGenerator
from .hari import Hari
from .struct_waktu import TimeSlot


# Contoh penggunaan dan testing
def main():
    # Initialize database
    db_manager = DatabaseManager("waktu_schedule.db")
    timeslot_manager = TimeSlotManager(db_manager)
    schedule_generator = ScheduleGenerator(timeslot_manager)

    # Bersihkan database sebelumnya (opsional)
    _ = timeslot_manager.clear_all_timeslots()

    print("=== GENERATING SCHEDULE ===")
    total_generated, results = schedule_generator.generate_schedule()

    print(f"Total timeslot generated: {total_generated}")
    print(f"Total attempts: {len(results)}")

    # Tampilkan hasil
    successes = [r for r in results if r[0]]
    failures = [r for r in results if not r[0]]

    print(f"\nSuccess: {len(successes)}")
    print(f"Failed (overlap): {len(failures)}")

    if failures:
        print("\nFailed entries (overlap):")
        for failure in failures[:5]:  # Tampilkan 5 pertama saja
            print(f"  - {failure[2]}")

    # Tampilkan jadwal yang berhasil disimpan
    print("\n=== SCHEDULE IN DATABASE ===")
    all_timeslots: list[TimeSlot] = timeslot_manager.get_all_timeslots()

    for timeslot in all_timeslots:
        print(
            # f"ID: {timeslot[0]}, Hari: {timeslot[1]}, Waktu: {timeslot[2]} - {timeslot[3]}"
            f"ID: {timeslot.id}, Hari: {timeslot.hari}, Waktu: {timeslot.mulai} - {timeslot.selesai}"
        )

    # Test menambahkan timeslot yang overlap
    print("\n=== TESTING OVERLAP VALIDATION ===")
    # success, timeslot_id, message = timeslot_manager.add_timeslot(
    success, _, message = timeslot_manager.add_timeslot(
        Hari.getId("Senin"), "08:30", "09:15"
    )
    print(f"Tambah timeslot overlap: {'Success' if success else 'Failed'} - {message}")

    # Test menambahkan timeslot yang valid
    # success, timeslot_id, message = timeslot_manager.add_timeslot(
    success, _, message = timeslot_manager.add_timeslot(
        Hari.getId("Senin"), "17:00", "17:45"
    )
    print(f"Tambah timeslot valid: {'Success' if success else 'Failed'} - {message}")


def export_to_csv(db_path: str = "waktu_schedule.db"):
    """Export data ke CSV untuk analisis"""
    import csv

    db_manager = DatabaseManager(db_path)
    timeslot_manager = TimeSlotManager(db_manager)

    timeslots: list[TimeSlot] = timeslot_manager.get_all_timeslots()

    with open("schedule_export.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Hari", "Start Time", "End Time", "Created At"])

        for timeslot in timeslots:
            writer.writerow(timeslot)

    print("Data berhasil diexport ke schedule_export.csv")


if __name__ == "__main__":
    main()
    # export_to_csv()  # Uncomment untuk export CSV
