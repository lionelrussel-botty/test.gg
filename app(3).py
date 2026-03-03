import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("円管内流れ：層流↔乱流 自動切替")

# ===== 入力 =====
R = st.slider("半径 R (m)", 0.01, 0.2, 0.05)
rho = st.slider("密度 ρ (kg/m^3)", 0.1, 2000.0, 1000.0)
mu = st.slider("粘性係数 μ (Pa·s)", 0.0001, 1.0, 0.001)
U = st.slider("平均流速 U (m/s)", 0.01, 5.0, 0.5)

D = 2*R
Re = rho * U * D / mu

r = np.linspace(-R, R, 300)

# ===== モデル切替 =====
if Re < 2300:
    flow_type = "Laminar"
    u = 2*U*(1 - (r**2)/(R**2))
else:
    flow_type = "Turbulent (1/7 power law)"
    umax = 1.22 * U
    u = umax*(1 - np.abs(r)/R)**(1/7)

# ===== 描画 =====
fig, ax = plt.subplots(figsize=(9,4))

# パイプ壁
ax.plot([0, 5], [R, R], 'k')
ax.plot([0, 5], [-R, -R], 'k')

# 速度分布
ax.plot(u, r, linewidth=2, label=flow_type)

# 矢印と数値
sample_r = np.linspace(-R, R, 7)

for rr in sample_r:
    if Re < 2300:
        u_val = 2*U*(1 - (rr**2)/(R**2))
    else:
        u_val = 1.22*U*(1 - abs(rr)/R)**(1/7)

    ax.arrow(0.2, rr, u_val*0.5, 0,
             head_width=0.03*R,
             head_length=0.1,
             fc='red', ec='red')

    ax.text(u_val*0.5 + 0.25, rr,
            f"{u_val:.2f}",
            fontsize=8,
            verticalalignment='center')

ax.set_ylim(-R, R)
ax.set_xlim(0, max(u)*0.6 + 0.5)
ax.set_xlabel("Velocity (m/s)")
ax.set_ylabel("Radius r")
ax.set_title("Side View of Pipe Flow")
ax.grid()
ax.legend()

st.pyplot(fig)

# ===== Reynolds表示 =====
st.subheader(f"Re = {Re:.0f}")

if Re < 2300:
    st.success("層流")
elif Re < 4000:
    st.warning("遷移領域")
else:
    st.error("乱流")