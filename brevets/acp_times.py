"""
Open and close time calculations for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders

# useful sites:
https://rusa.org/pages/acp-brevet-control-times-calculator
https://rusa.org/octime_acp.html

# Total Race Times:
200 kilometres (120 mi) - 13.5 hours (15 km/h)
300 kilometres (190 mi) - 20 hours (15 km/h)
400 kilometres (250 mi) - 27 hours (15 km/h)
600 kilometres (370 mi) - 40 hours (15 km/h)
1,000 kilometres (620 mi) - 75 hours (13.3 km/h)
1,200 kilometres (750 mi) - 90 hours (13.3 km/h)
1,400 kilometres (870 mi) - 116:40 hours (12 km/h)
2,200 kilometres (1,400 mi) - 220 hours (10 km/h)

# Oddities:
for any control(checkpoint) at 60km or less, divide dist by 20 and then add 1 hour
"""

import arrow
import math

# store total time of race (in hours) based on brevet distance
finish_times = {
   200: 13.5,
   300: 20,
   400: 27,
   600: 40,
   1000: 75,
}

# these two fxns are called every time someone enters a new checkpoint
def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object

    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    
    bin_subs = [200/34, 200/32, 200/30, 400/28]    # fastest time for each bin to subtract

    # race start
    if (control_dist_km == 0):
      return brevet_start_time

    # clamp controls to total race distance
    if (control_dist_km > brevet_dist_km):
      control_dist_km = brevet_dist_km
   
    # 0 - 200
    if (control_dist_km <= 200):
      val = (control_dist_km / 34)
      hours = math.floor(val)
      mins = round((val % 1) * 60)
      return brevet_start_time.shift(hours=hours, minutes=mins)

    # 200 - 400
    if (control_dist_km >= 200 and control_dist_km <= 400):
      # get distance travelled in THIS bin
      dist = (control_dist_km - 200)

      # add on fastest time of previous bin(s)
      val = bin_subs[0] + (dist / 32)

      hours = math.floor(val)
      mins = mins = round((val % 1) * 60)
      return brevet_start_time.shift(hours=hours, minutes=mins)
   
    # 400 - 600
    if (control_dist_km >= 400 and control_dist_km <= 600):
      # get distance travelled in THIS bin
      dist = (control_dist_km - 400)

      # add on fastest time of previous bin(s)
      val = bin_subs[0] + bin_subs[1] + (dist / 30)
      
      hours = math.floor(val)
      mins = mins = round((val % 1) * 60)
      return brevet_start_time.shift(hours=hours, minutes=mins)
   
    # 600 - 1000
    if (control_dist_km >= 600 and control_dist_km <= 1000):
      # get distance travelled in THIS bin
      dist = (control_dist_km - 600)

      # add on fastest time of previous bin(s)
      val = bin_subs[0] + bin_subs[1] +  bin_subs[2] + (dist / 28)

      hours = math.floor(val)
      mins = mins = round((val % 1) * 60)
      return brevet_start_time.shift(hours=hours, minutes=mins)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object

    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    # first checkpoint always closes after 1 hour
    if (control_dist_km == 0):
      return brevet_start_time.shift(hours=1)

    # races end at pre-defined times based on total distance
    if (control_dist_km >= brevet_dist_km):
      return brevet_start_time.shift(hours=finish_times[brevet_dist_km])

    # apply special rule for dist <= 60
    if (control_dist_km <= 60):
      val = (control_dist_km / 20)
      hours = math.floor(val) + 1
      mins = round((val % 1) * 60)
      return brevet_start_time.shift(hours=hours, minutes=mins)
   
    # 0 - 600 (first three bins have same min speed)
    if (control_dist_km <= 600):
      val = (control_dist_km / 15)
      hours = math.floor(val)
      mins = round((val % 1) * 60)
      return brevet_start_time.shift(hours=hours, minutes=mins)
   
    # 600 - 1000
    if (control_dist_km >= 600 and control_dist_km <= 1000):
      # get distance travelled in THIS bin
      dist = (control_dist_km - 600)

      # add on slowest time of previous bin(s)
      val = (600 / 15) + (dist / 11.428)

      hours = math.floor(val)
      mins = mins = round((val % 1) * 60)
      return brevet_start_time.shift(hours=hours, minutes=mins)
