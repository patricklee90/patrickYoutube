# website: https://vhernando.github.io/calculate-pi-digits-python-high-precision
# explanation: https://www.mathscareers.org.uk/calculating-pi/

import json
import sys
from datetime import datetime, timedelta
from decimal import Decimal, getcontext


def calculate_pi(precision, stat=True):

    excess_prec = 2

    prec_cur = precision if precision > 100 else 100

    if not stat:
        prec_cur = precision

    getcontext().prec = prec_cur + excess_prec
    second = Decimal(3)  # Current element for PI

    queue_cur = [Decimal(0), Decimal(0), Decimal(0), second]

    qq_append = queue_cur.append
    qq_pop = queue_cur.pop

    limit = Decimal(10) ** (-prec_cur - excess_prec)

    while True:
        sec_sq = second * second
        term = second
        acc = second + term
        count = Decimal(1)

        while term > limit:

            term *= sec_sq / ((count + 1) * (count + 2))
            acc -= term
            # print("term1: {}".format(term))

            term *= sec_sq / ((count + 3) * (count + 4))
            acc += term

            count += 4
            # print("term2: {}".format(term))

        # print ('acc: {}'.format(second))
        if acc in queue_cur:
            if prec_cur < precision:
                prec_cur += prec_cur
                if prec_cur > precision:
                    prec_cur = precision
                limit = Decimal(10) ** (-prec_cur - excess_prec)
                getcontext().prec = prec_cur + excess_prec

            else:
                second = acc
                break

        qq_append(acc)
        qq_pop(0)
        second = acc
        # print ('second: {}'.format(second))

        return second


if len(sys.argv) < 2:
    print("Not enough arguments, it enter preset mode")
    pi_seq = [
        # 10,
        # 100,
        # 500,
        # 1000,
        # 5000,
        # 10000,
        # 30000,
        # 60000,
        90000,
        100000,
        1000000,
        10000000,
        100000000,
        1000000000,
    ]

    for seq in pi_seq:
        start = datetime.now()
        print(f"decimal length: {seq} at time {start}")
        result = {
            "decimal": seq,
            "startTime": start.isoformat(),
            "endTime": 0,
            "duration": 0,
        }
        second = calculate_pi(seq, False)

        result["endTime"] = datetime.now().isoformat()
        result["duration"] = str(datetime.now() - start)
        with open(f"{seq}_seq.json", "w") as outfile:
            json.dump(result, outfile, sort_keys=True, indent=4)

        with open(f"{seq}_pi.txt", "w") as outfile:
            outfile.write(str(second))
else:
    calculate_pi(int(sys.argv[1]))
    precision = int(sys.argv[1])
    second = calculate_pi(precision)
    getcontext().prec = precision
    print("PI: ", +second)
