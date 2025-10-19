waktu_data = []
waktu_id = 1

durasi = 45

waktu_mulai = '08:00'

for hari in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']:
    jam, menit = map(int, waktu_mulai.split(':'))

    a = 0

    while jam < 17:
        jam_mulai_obj = jam * 60 + menit
        jam_selesai_obj = jam_mulai_obj + 45

        start_h, start_m = divmod(jam_mulai_obj, 60)
        end_h, end_m = divmod(jam_selesai_obj, 60)

        jam = end_h
        menit = end_m

        if jam == 12: continue

        data = (waktu_id, hari, f"{start_h:02d}:{start_m:02d}", f"{end_h:02d}:{end_m:02d}")
        print(data)

        # waktu_data.append(data)
        waktu_id += 1

# print(waktu_data)
