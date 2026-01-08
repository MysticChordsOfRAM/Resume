import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from flask import Flask, render_template, send_file
import supersecrets as shh

app = Flask(__name__)

pc_photos = [
    {"file": "last_day.webp",
     "title": "My Last Day",
     "caption": (
        "This was my last day in the community. Some of my older students came out to help me pack "  
        "and finish up our world map mural. We got it done just in time for me to reach the city before dark."
    )},

    {"file": "fishing_boat.webp",
     "title": "Out at Sea",
     "caption": (
        "My community was a fishing village on the eastern coast. That introduced its own interesting dynamic to my service. "
        "For one thing, fishing is profitable. A lot of boys, after turing 15ish, start taking time off school to go fish, then realize "
        "they don't really need to go back. For another thing, it means the entire community is ruled by the fishing season. When the "
        "season is on, fishermen from all over the country descend on the town. They bring money, but they also bring a level of chaos and "
        "unpredictablility. Community censure is one of the strongest detterents they have against crime, but it's not terribly effective on "
        "people from outside the community."
    )},

    {"file": "class_time.webp",
     "title": "Class Time",
     "caption": (
       "Not lesson time, but class time. This is Class 2B, between lessons. Class 2 is roughly the equivalent of our 7th grade but I want to "
       "emphasize ~rough~. Students in this class range from 12 to 21 years old and most of them don't know multiplication or speak english (by "
       "this point, the official curriculum calls for them to be learning algebra and rhetoric - that's not gonna happen). The real value of their "
       "education isn't book learning but discipline and citizenship. And you can see that here. Even though it's not lesson time, everyone is seated "
       "and the goofing off is relatively tame. And don't judge the nappers too harshly - many of them have been up since before dawn doing chores "
       "for their house, then chores for the school (no janitor, the students clean the campus), and they know the real value of a break." 
    )},

    {"file": "school_contest.webp",
     "title": "Competition!",
     "caption": (
         "The school held an Academic Decathalon about halfway through my first year. One student from each grade per team, the A team is pictured."
         "Don't mistake a general lack of academic accomplishment for unintelligence. Delight (front, age 11) and Doe Stephen (back, tan shirt, age 19) "
         "are both wicked smart, and the B team is no slouch either. These students love a good showdown, and for two hours the entire student body "
         "crammed around as 6 kids battled for academic superiority. I only wish I could remember who won."
    )},

    {"file": "that_bird.webp",
     "title": "That Bird!",
     "caption": (
        "When I was in my first couple months on site we had a really bad overnight storm. The wind and the rain pummeled "
        "the coast for what must've been hours. At this point, I was still in the habit of waking up extra early and getting to the school well "
        "ahead of the other teachers, so as I arrived to campus the students were just starting to clean up the fallen branches and detritus that "
        "had been knocked around by wind. As I wandered around the buildings, making sure they were dry enough for lessons, I found some young kids "
        "huddled around a bit of chickenwire on the ground. In the chickenwire was this bird! They had captured it and planned to cook it. I was, "
        "of course, horrified, that someone could find this bird, stunned and weak from the storm, and think to eat it. So I rescued it from the kids "
        "and tried to release it. But it didn't want to go anywhere. I ended up teaching my morning classes with this dumb bird on my hand. " 
        "Around lunchtime, I took it for a walk in the marshy area behind the school and it finally honked at me and flew off. My next class "
        "was so disapointed when I didn't bring the bird to their lesson, that one of them went out and caught me a pigeon! When I told him that I "
        "didn't want it, they proceeded to kill it and cook it. Lesson Learned."
     )},

    {"file": "fitness_day.webp",
     "title": "Fitness Day",
     "caption": (
         "Lessons were always getting cancelled for one thing or another. This day, the headmaster decided we would have a \"Fitness Day\" to "
         "teach students how to excercise. For me, any activity day is a day for me to bring my camera and get embarrasing candid shots of "
         "my students, so my complaints were minimal. The kids, bless them, always hammed it up for the camera, but Gideon's efforts in this "
         "shot are a level above. He launched into this pose out of his plank without any thought for how he would land. "
         "Bruises well earned! I only wish I had closed the shutter half a second later to get everyone's reactions."
     )},

    {"file": "computer_class.webp",
     "title": "Computer Class",
     "caption": (
        "Computer Class was made possible by Mr. Tay, who would bring in his own computer, peripherals, and extension cord for practicals. "
        "The school has been the recipient of donated laptops on at least three occasions, but the salty air, heat, and dust kill them with "
        "remarkable speed. Mr. Tay keeps this machine clean and maintained on his own, so the kids have something to learn on. This is just one "
        "example of many where the charity of others fails to make its proper impact due to poor planning. Until the school has an air-conditioned "
        "and weather sealed room, donated laptops will continue to fail. But it's much easier to get donated laptops than to build such a room "
        "so I expect the flow of laptops to continue, and for Mr. Tay to need to fill the gaps with his own efforts."
    )}
]

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
    ax.axis('off')

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
    return render_template('homepage.html', photos = pc_photos)

if __name__ == "__main__":
    app.run(host = shh.app_host, port = shh.app_port)
