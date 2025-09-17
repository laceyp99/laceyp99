import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection

fs = 44100
duration = 10
t = np.linspace(0, duration, fs * duration)
window_size = 1000  # Wider window for full width

# Envelope for intensity: intense → calm → intense
def envelope(tt):
    # 0-1: intense, 1-7: calm, 7-10: intense
    env = np.ones_like(tt)
    env[(tt > 1) & (tt < 7)] = 0.4 + 0.2 * np.sin((tt[(tt > 1) & (tt < 7)]-1)*np.pi/6)
    env[tt >= 7] = 1.0
    return env

base = 1.2 * np.sin(2 * np.pi * 50 * t)  # 808 bass
kick = 0.7 * np.exp(-5 * (t % 1)) * np.sin(2 * np.pi * 60 * t)  # punchy kick
hi = 0.3 * np.sin(2 * np.pi * 800 * t)  # hi-hat shimmer
noise = 0.1 * np.random.randn(len(t))
wave = (base + kick + hi + noise) * envelope(t)

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, window_size - 1)
ax.set_ylim(-2, 2)
ax.axis("off")
ax.margins(0)  # Remove all margins
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove padding around the plot
fig.patch.set_facecolor("#411B1B")
ax.set_facecolor("#271B13")

# Color gradient for waveform (keep your colors)
def get_gradient_colors(n):
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("audiofeed",
        ["#067620", "#eef134", "#cd8c00", "#e4683f", "#c605059a"])
    return cmap(np.linspace(0, 1, n))

def make_waveform_line(x, y):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    colors = get_gradient_colors(len(x)-1)
    lc = LineCollection(segments, colors=colors, linewidth=4, alpha=0.95)
    return lc

current_lc = None

def init():
    global current_lc
    if current_lc:
        current_lc.remove()
    current_lc = None
    return []

def update(frame):
    global current_lc
    start = frame
    end = frame + window_size
    x = np.arange(window_size)
    y = wave[start:end]
    lc = make_waveform_line(x, y)
    if current_lc:
        current_lc.remove()
    current_lc = ax.add_collection(lc)
    return [current_lc]

ani = animation.FuncAnimation(
    fig, update, frames=range(0, len(wave) - window_size, 200),
    init_func=init, blit=True, interval=30, repeat=True
)

ani.save("assets/waveform.gif", writer="pillow", fps=30)