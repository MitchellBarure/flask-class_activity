#plotter.py

import base64
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt #matplotlib is used to create the graph


def make_graph_base64(sizes, times):
    plt.figure()
    plt.plot(sizes, times)
    plt.xlabel("Input size (n)")
    plt.ylabel("Time (ms)")
    plt.title("Algorithm Runtime")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)
    image_bytes = buffer.read()
    buffer.close()

    return base64.b64encode(image_bytes).decode("utf-8")
