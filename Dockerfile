#Χρησιμοποιώ μια ελαφριά εικόνα του Python 3.10 ως βάση για το Docker container μου.
FROM python:3.10-slim
# Ορίζω το working directory μέσα στο container.
WORKDIR /app
# Αντιγράφω το αρχείο requirements.txt στο working directory του container.
COPY requirements.txt .
# Τρέχω την εντολή pip install για να εγκαταστήσω τις εξαρτήσεις που αναφέρονται στο requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
# Αντιγράφω όλα τα αρχεία από το τρέχον directory στον φάκελο /app του container.
COPY . .
# Δημιουργώ έναν φάκελο για logs ή output αν χρειάζεται.
RUN mkdir -p outputs
#Xρησιμοποιώ την εντολή ENTRYPOINT ώστε να μπορώ να περνάω παραμέτρους κατά την εκτέλεση του container, αν χρειάζεται.
ENTRYPOINT ["python", "run.py"]
# Ορίζω την προεπιλεγμένη εντολή που θα εκτελείται όταν το container ξεκινάει.
CMD ["--profile", "profiles/demo.yaml"]
