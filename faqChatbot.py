import pandas as pd
from fuzzywuzzy import fuzz

df = pd.read_csv('chatbot_faq_dataset(HR_FAQ).csv', encoding='utf-8')

best_t = 63

def get_faq_answer(question, faq_df=df, threshold=best_t):
    """
    Finds the best matching answer for a given question from the FAQ dataframe.

    Args:
        question (str): The user's question.
        faq_df (pd.DataFrame): The dataframe containing FAQ questions and answers.
        threshold (int): The minimum fuzzy matching score to consider a match.

    Returns:
        str: The best matching answer or a fallback message if no good match is found.
    """
    best_match_score = 0
    best_match_answer = "Maaf, saya tidak menemukan jawaban yang relevan untuk pertanyaan Anda. Silakan coba formulasi pertanyaan lain atau hubungi tim HR."

    for index, row in faq_df.iterrows():
        # Ensure the 'Questions' column is treated as a string for fuzzy matching
        faq_question = str(row['Questions'])
        score = fuzz.ratio(question.lower(), faq_question.lower())

        if score > best_match_score and score >= threshold:
            best_match_score = score
            best_match_answer = row['Answers']

    return best_match_answer

def tune_fuzzy_threshold(faq_df, training_data):
    """
    Optimizes the fuzzy matching threshold using a given training dataset.

    Args:
        faq_df (pd.DataFrame): The dataframe containing canonical FAQ questions and answers.
        training_data (list of tuples): A list where each tuple is
                                        (user_question_variation, expected_answer).

    Returns:
        tuple: (best_threshold, highest_accuracy)
    """
    if not training_data:
        print("Warning: No data provided.")
        return None, 0.0

    print(f"Starting tuning fuzzy threshold using {len(training_data)} training examples...")

    best_threshold = 0
    highest_accuracy = 0.0

    # Iterate through possible thresholds from 0 to 100
    for current_threshold in range(0, 101):
        correct_matches = 0
        total_questions = len(training_data)

        for user_q_variant, expected_answer in training_data:
            # Get the best match using the current threshold
            matched_answer = get_faq_answer(user_q_variant, faq_df, current_threshold)

            # Check if the matched answer is the expected one
            if matched_answer == expected_answer:
                correct_matches += 1

        accuracy = (correct_matches / total_questions) * 100

        if accuracy > highest_accuracy:
            highest_accuracy = accuracy
            best_threshold = current_threshold

        print(f"  Threshold {current_threshold}: Accuracy = {accuracy:.2f}%")

    print("\nTuning complete!")
    print(f"Best Threshold: {best_threshold} (Accuracy: {highest_accuracy:.2f}%)")
    return best_threshold

training_data_examples = [
    ("Bagaimna cara agsr saya bisa cuti?", "Pengajuan cuti dapat dilakukan melalui sistem HRIS internal atau dengan mengisi formulir cuti manual yang disetujui oleh atasan langsung. Idealnya, permohonan dilakukan minimal 3 hari kerja sebelumnya, kecuali dalam keadaan darurat. Di perusahaan besar seperti BUMN, sistem pengajuan cuti terintegrasi dengan kalender kerja organisasi agar jadwal kerja tim tetap efisien dan tidak tumpang tindih. HR akan membantu mencatat dan memverifikasi proses ini."),
    ("Apa warna bulan?", "Maaf, saya tidak menemukan jawaban yang relevan untuk pertanyaan Anda. Silakan coba formulasi pertanyaan lain atau hubungi tim HR."),
    ("Bagaimana cara saya melihat sisa cuty saya?", "Anda bisa mengecek sisa cuti tahunan dan cuti lainnya melalui sistem HRIS. Jika Anda mengalami kesulitan mengaksesnya, silakan hubungi HR langsung. Jumlah cuti yang tersisa biasanya diperbarui secara otomatis setelah permintaan cuti disetujui. Kami mendorong Anda untuk merencanakan cuti dengan bijak demi menjaga keseimbangan kerja dan kehidupan pribadi."),
    ("Apakah gaji lembur saya akan kena pajsk?", "Ya, sesuai peraturan perpajakan Indonesia, seluruh penghasilan termasuk upah lembur merupakan objek pajak dan akan dikenai Pajak Penghasilan (PPh 21). Namun, potongannya telah dihitung otomatis oleh sistem payroll perusahaan. Di BUMN, transparansi pemotongan ini bisa dicek melalui slip gaji atau sistem HRIS."),
    ("Bagaimana jika saya terlambat datang kerja?", "Kami memahami bahwa keterlambatan bisa terjadi. Namun, Anda wajib memberi kabar ke atasan atau tim HR sesegera mungkin. Terlambat tanpa pemberitahuan akan tercatat sebagai pelanggaran disiplin kerja. Dalam kondisi tertentu, keterlambatan bisa dimaafkan dengan alasan yang jelas."),
    ("Kapan hari jadi kota bandung?", "Maaf, saya tidak menemukan jawaban yang relevan untuk pertanyaan Anda. Silakan coba formulasi pertanyaan lain atau hubungi tim HR."),
    ("Apa saya boleh bekerja dari rumsh?","Kemungkinan bekerja dari rumah (WFH) sangat tergantung pada jenis pekerjaan dan kebijakan unit kerja masing-masing. Di beberapa BUMN, sistem kerja fleksibel seperti hybrid atau remote sudah mulai diadopsi terutama setelah pandemi, dengan tetap mengedepankan produktivitas. Jika posisi Anda memungkinkan, Anda bisa mengajukan WFH melalui atasan dan mengikuti mekanisme pelaporan kerja harian yang telah ditentukan."),
    ("Bagaimama proses kinerja saya dinilai?","Penilaian kinerja karyawan dilakukan melalui Performance Management. Performance management adalah sistem pengelolaan kinerja karyawan yang selaras dengan strategi perusahaan. Di Telkom, performance management diturunkan dari Corporate Strategic Scenario (CSS) hingga ke Kontrak Manajemen (KM), yang menjadi dasar pengukuran kinerja individu. "),
    ("Apakah nanti ada evaluasi kesrhatan rutin?","Ya, sebagian besar BUMN menyediakan Medical Check Up (MCU) rutin setiap tahun atau dua tahun sekali. Ini dilakukan sebagai upaya preventif untuk menjaga kesehatan pegawai dan mendeteksi dini potensi gangguan kesehatan akibat pekerjaan. Anda akan dijadwalkan untuk mengikuti MCU oleh HR, dan hasilnya akan disampaikan secara rahasia kepada Anda."),
    ("Apakah saya boleh tidur?", "Maaf, saya tidak menemukan jawaban yang relevan untuk pertanyaan Anda. Silakan coba formulasi pertanyaan lain atau hubungi tim HR."),
    ("Apakah perusahaan membayarkan bpjs saya?","Ya, perusahaan menanggung sebagian besar iuran BPJS Kesehatan dan BPJS Ketenagakerjaan sesuai ketentuan pemerintah. Anda akan melihat potongan gaji kecil sebagai kontribusi wajib pekerja. Ini sesuai dengan Perpres No. 82 Tahun 2018 dan UU No. 24 Tahun 2011."),
    ("Bagaimana perpanjangan kontrak karyawan?","Perpanjangan kontrak dilakukan berdasarkan evaluasi kinerja dan kebutuhan unit kerja. Karyawan kontrak yang menunjukkan performa baik akan mendapatkan kesempatan untuk diperpanjang kontraknya atau bahkan diangkat menjadi pegawai tetap jika tersedia formasi. Sesuai dengan PP No. 35 Tahun 2021, hubungan kerja kontrak harus dicatat secara tertulis, dan perusahaan wajib memberikan kejelasan sebelum kontrak berakhir."),
    ("Bagaimana kalau saya sakit lebih dari satu hari?","Ya, selama Anda memberikan surat keterangan dokter atau rumah sakit, maka gaji Anda tetap dibayarkan secara penuh. Hal ini sesuai dengan Pasal 93 UU No. 13 Tahun 2003, yang menyatakan bahwa pekerja tidak kehilangan hak atas upah jika tidak masuk karena alasan sah, termasuk sakit. Di perusahaan BUMN, validasi cuti sakit dilakukan secara administratif oleh HR agar seluruh proses tetap transparan dan tidak merugikan pegawai. Kesehatan Anda adalah prioritas, jadi jangan ragu untuk beristirahat jika dibutuhkan."),
    ("Bolehkan saya meminjam uang sepuluh ribu?", "Maaf, saya tidak menemukan jawaban yang relevan untuk pertanyaan Anda. Silakan coba formulasi pertanyaan lain atau hubungi tim HR."),
    ("Siapa presiden ke-tujuh Indonesia?", "Maaf, saya tidak menemukan jawaban yang relevan untuk pertanyaan Anda. Silakan coba formulasi pertanyaan lain atau hubungi tim HR."),
    ("Apa ada pelatihan untuk karyawsn?","Ya, perusahaan menyediakan program pelatihan berkala baik secara internal maupun eksternal. Ini bisa berupa pelatihan teknis, soft skill, kepemimpinan, hingga sertifikasi tertentu. Dalam Telkom, pengajuan mengikuti program pelatihan dilakukan melalui HCSP / AM EBIS kepada Telkom Corporate University Center, berdasarkan rencana pengembangan kompetensi individu (IDP) atau kebutuhan unit kerja. Output dari pelatihan berupa sertifikat pelatihan, peningkatan kompetensi, dan pencatatan data pengembangan SDM.	"),
    ("Berapa besasar thr saya?","Besarnya THR umumnya setara dengan satu kali gaji pokok bagi karyawan yang telah bekerja selama 12 bulan secara penuh. Jika masa kerja Anda belum genap setahun, maka perhitungannya dilakukan secara proporsional sesuai masa kerja. Ketentuan ini tertuang dalam Permenaker No. 6 Tahun 2016 Pasal 3, dan di perusahaan milik negara, pembayaran THR biasanya dikelola secara terpusat untuk memastikan tidak ada keterlambatan dan seluruh pegawai menerima haknya sesuai regulasi."),
    ("apakah ada kemungkinan saya pindah divisi?","Ya, perpindahan divisi bisa dilakukan atas dasar kebutuhan organisasi atau inisiatif karyawan. Jika Anda merasa tidak cocok di posisi saat ini, Anda bisa berkonsultasi dengan atasan atau HR untuk menilai kemungkinan mutasi. Di BUMN, mobilitas internal justru dianggap sebagai bagian dari proses pengembangan karier."),
    ("apakah karyawan tetap bisa keluard?","Ya, karyawan tetap bisa diberhentikan, tetapi prosesnya harus melalui tahapan yang jelas dan adil sesuai dengan ketentuan perundang-undangan. Berdasarkan UU No. 13 Tahun 2003 Pasal 151, perusahaan wajib mengupayakan penyelesaian secara musyawarah terlebih dahulu. Alasan pemutusan hubungan kerja (PHK) harus didasarkan pada pelanggaran berat, efisiensi, atau alasan hukum lainnya yang sah. Di lingkungan BUMN, proses PHK juga diawasi ketat oleh manajemen dan harus disetujui oleh dewan pengawas atau regulator internal."),
    ("apa fasilitas kesetatan yang diberikan untuk saya?","Perusahaan memberikan fasilitas BPJS Kesehatan dan BPJS Ketenagakerjaan, serta subsidi medical check-up tahunan. Untuk klaim kesehatan tambahan, silakan cek detail asuransi jika perusahaan bekerja sama dengan provider tertentu.")
]

# best_t = tune_fuzzy_threshold(df, training_data_examples)