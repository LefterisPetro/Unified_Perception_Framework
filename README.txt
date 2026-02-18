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

(18/2)
Το UPF τώρα έχει:
--Core
EventBus
Runner
Typed BaseEvent
Deterministic event types

--Payload Layer
Strict Pydantic models
Fully nested typed chain
No dynamic schema guessing

--Plugin Layer
Modular processors
Config-driven instantiation
Strict constructor validation

--Boundary Layer
Centralized serialization helper
Clean sink abstraction
Stable output