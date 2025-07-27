from sqlalchemy import create_engine, text
import pandas as pd
import random
import time
import os
db_path = os.path.abspath("grid.db")
engine = create_engine(f"sqlite:///{db_path}", future=True)
print("init_db writing to:", db_path)
seed_data = pd.DataFrame({
    "zone": list(range(1, 8)),
    "fault_triggered": ["No"] * 7,
    "load_lost": [0] * 7,
    "blackout_time": [0.0] * 7,
    "recovery_time": [0.0] * 7,
    "power_restored": [100] * 7,
    "resilience_score": [10.0] * 7
})

with engine.begin() as conn:
    seed_data.to_sql("resilience_data", con=conn, if_exists="replace", index=False)
def random_update():
    z = random.randint(1, 7)
    fault = "Yes" if random.random() < 0.6 else "No"
    load_lost = random.randint(100, 500) if fault == "Yes" else 0
    blackout = round(random.uniform(1.0, 4.0), 2) if fault == "Yes" else 0.0
    recovery = round(blackout + random.uniform(1.0, 2.0), 2) if fault == "Yes" else 0.0
    restored = max(80, 100 - load_lost // 5)
    score = round(max(0, min(10, 10 - load_lost / 100 - blackout / 5)), 2)

    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE resilience_data
                SET fault_triggered = :fault,
                    load_lost = :ll,
                    blackout_time = :bt,
                    recovery_time = :rt,
                    power_restored = :pr,
                    resilience_score = :rs
                WHERE zone = :z
            """),
            {
                "fault": fault,
                "ll": load_lost,
                "bt": blackout,
                "rt": recovery,
                "pr": restored,
                "rs": score,
                "z": z
            }
        )

    print(f"Updated Zone {z} | Fault: {fault} | Load Lost: {load_lost} kW | Score: {score}/10")
if __name__ == "__main__":
    print(" Simulating real-time updates every 15 seconds")
    try:
        while True:
            random_update()
            time.sleep(15)
    except KeyboardInterrupt:
        print(" Stopped")

