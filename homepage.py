import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from flask import Flask, render_template, send_file
import supersecrets as shh

app = Flask(__name__)

@app.route('/logo.png')
def dynamic_logo():
    n_points = 15000

    circle_h, circle_k, circle_r = 50, 50, 48

    h, k = 23, 50
    out_a, out_b = 30, 30
    n = 3
    stroke_thick = 6
    in_a, in_b = out_a - stroke_thick, out_b - stroke_thick

    stem_width = 12
    bar_length = 25
    kerning = 5

    i_top = k + out_b
    i_bottom = k - out_b
    i_start = h + out_a + kerning
    i_center = i_start + (bar_length / 2)

    x = np.random.uniform(0, 100, n_points)
    y = np.random.uniform(0, 100, n_points)
    z = np.random.uniform(0, 100, n_points)

    dist_center = np.sqrt((x - circle_h)**2 + (y - circle_k)**2)

    mask_circle = dist_center <= circle_r

    d_term_x = (np.abs(x - h) / out_a)**n
    d_term_y = (np.abs(y - k) / out_b)**n
    mask_outer_d = (d_term_x + d_term_y <= 1) & (x > h)

    d_in_term_x = (np.abs(x - h) / in_a)**n
    d_in_term_y = (np.abs(y - k) / in_b)**n
    mask_d_inner = (d_in_term_x + d_in_term_y <= 1) & (x > h)

    mask_d_stem = (x >= (h - stem_width / 2)) & (x <= h) & (y >= i_bottom) & (y <= i_top)

    mask_d = (mask_outer_d | mask_d_stem) & (~mask_d_inner)

    mask_i_top = (x >= i_start) & (x <= i_start + bar_length) & (y >= i_top - stem_width/2) & (y <= i_top)
    mask_i_bottom = (x >= i_start) & (x <= i_start + bar_length) & (y >= i_bottom) & (y <= i_bottom + stem_width/2)
    mask_i_stem = (x >= i_center - stem_width/4) & (x <= i_center + stem_width/4) & (y >= i_bottom) & (y <= i_top)

    mask_i = mask_i_top | mask_i_bottom | mask_i_stem

    mask_keep = mask_circle & (~mask_d) * (~mask_i)

    x_final = x[mask_keep]
    y_final = y[mask_keep]
    z_final = z[mask_keep]
    dist_final = dist_center[mask_keep]

    mask_outlier = np.random.rand(len(x_final)) < 0.0025

    fig, ax = plt.subplots(figsize = (6, 6))

    cmap = LinearSegmentedColormap.from_list("devlin_green", ["#091050", "#98afec"])

    ax.scatter(
        x_final[~mask_outlier],
        y_final[~mask_outlier],
        c = z_final[~mask_outlier],
        cmap = cmap,
        marker = 's',
        s = 15,
        alpha = 1 - (dist_final[~mask_outlier]/circle_r * 0.7),
        edgecolors = 'none'
    )

    ax.scatter(
        x_final[mask_outlier],
        y_final[mask_outlier],
        c = "#720707",
        marker = 's',
        s = 35,
        alpha = 1,
        edgecolors = 'none'
    )

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')
    #ax.axis('off')

    buf = io.BytesIO()

    plt.savefig(buf, 
                format='png', 
                transparent = True, 
                bbox_inches = 'tight', 
                pad_inches = 0)
    
    buf.seek(0)
    plt.close(fig)

    return send_file(buf, mimetype = 'image/png')


@app.route('/')
def homepage():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run(host = shh.app_host, port = shh.app_port)
