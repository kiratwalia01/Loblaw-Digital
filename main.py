import argparse
import time

import pandas as pd
from PIL import Image


def get_image_sim_exec_time(ip1, ip2):
    start_time = time.time()
    i1, i2 = Image.open(ip1), Image.open(ip2)

    if i1.mode != i2.mode or i1.size != i2.size:
        return "Error", round(time.time() - start_time, 2)

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    n_components = i1.size[0] * i1.size[1] * 3
    return str((dif / 255.0) / n_components), round(time.time() - start_time, 2)


def get_sim(fp, out_fp):
    try:
        df = pd.read_csv(fp, header=0)
        sims, exec_times = list(), list()
        for _, row in df.iterrows():
            sim, exec_time = get_image_sim_exec_time(row["image1"], row["image2"])
            sims.append(sim)
            exec_times.append(exec_time)
        df['similar'] = sims
        df['elapsed'] = exec_times
        df.to_csv(out_fp)
    except Exception as e:
        print("there is some error:", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip_file', help='Input CSV file path', required=True)
    parser.add_argument('-op_file', help='Output CSV file path', required=True)
    args = vars(parser.parse_args())
    get_sim(args['ip_file'], args['op_file'])
