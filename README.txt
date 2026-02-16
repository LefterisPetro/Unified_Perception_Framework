Unified_Perception_Framework

(15/2)Μέχρι τώρα έχουμε runtime που:
- Τρέχει πολλαπλές async πηγές
- Δρομολογεί events με βάση τύπο
- Επιτρέπει stateful processing
- Υποστηρίζει πολλαπλά outputs
- Μπορεί να  επεκταθεί χωρίς να πειράξουμε core

(16/2)
Μέχρι τώρα το run.py ήταν hardcoded και σήμερα θα το κάνουμε
Profile-Driven runtime 
Δηλαδή python run.py --profile irrigation
       python run.py --profile wildfire
       python run.py --profile demo

και να αλλάζει όλο το pipeline χωρίς να πειράζουμε τον κώδικα.

