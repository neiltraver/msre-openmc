import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

T, k, sd = np.loadtxt("sweep_results.csv", delimiter=",", skiprows=1, unpack=True)

rho = (k - 1) / k * 1e5          # reactivity in pcm
rho_err = sd / k**2 * 1e5        # propagated uncertainty

# fit over the physically defensible window (500-700 C)
m = T <= 700
p, cov = np.polyfit(T[m], rho[m], 1, cov=True)
alpha, alpha_err = p[0], np.sqrt(cov[0, 0])

print(f"alpha (500-700 C) = {alpha:.2f} +/- {alpha_err:.2f} pcm/degC")
for t, r, e in zip(T, rho, rho_err):
    print(f"{t:6.0f} C   rho = {r:8.1f} +/- {e:5.1f} pcm")

plt.errorbar(T, rho, yerr=rho_err, fmt="o", capsize=3, label="simulation")
plt.plot(T[m], np.polyval(p, T[m]), "-",
         label=f"fit 500-700 C: {alpha:.1f} pcm/$\\degree$C")
plt.axhline(0, color="gray", lw=0.5)
plt.xlabel("Fuel salt temperature (°C)")
plt.ylabel("Reactivity (pcm)")
plt.title("MSRE temperature coefficient of reactivity")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("reactivity_vs_temperature.png", dpi=150, bbox_inches="tight")
print("saved reactivity_vs_temperature.png")