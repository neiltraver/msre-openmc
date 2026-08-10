import os, glob, subprocess
import openmc

TEMPERATURES = list(range(500, 1001, 50))
RESULTS = "sweep_results.csv"

if not os.path.exists(RESULTS):
    with open(RESULTS, "w") as f:
        f.write("salt_temp_C,k_combined,k_std_dev\n")

done = set()
with open(RESULTS) as f:
    next(f)
    for line in f:
        if line.strip():
            done.add(float(line.split(",")[0]))

for T in TEMPERATURES:
    if float(T) in done:
        print(f"skip {T} C (already done)", flush=True)
        continue

    for old in glob.glob("statepoint.*.h5"):
        os.remove(old)

    print(f"=== running salt_temp = {T} C ===", flush=True)
    env = dict(os.environ, SALT_TEMP=str(T))
    if subprocess.run(["python", "msre_critical.py"], env=env).returncode != 0:
        print(f"run failed at {T} C - stopping", flush=True)
        break

    sp_files = glob.glob("statepoint.*.h5")
    if not sp_files:
        print(f"no statepoint at {T} C - stopping", flush=True)
        break

    with openmc.StatePoint(sp_files[0]) as sp:
        k, sd = sp.keff.nominal_value, sp.keff.std_dev

    os.rename(sp_files[0], f"statepoint_T{T}.h5")
    with open(RESULTS, "a") as f:
        f.write(f"{T},{k:.6f},{sd:.6f}\n")
    print(f"=== {T} C: k = {k:.5f} +/- {sd:.5f} ===", flush=True)

print("sweep complete", flush=True)