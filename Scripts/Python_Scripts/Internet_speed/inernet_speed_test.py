###############################################
# Date:         2026-09-08
# Script Name:  internet_speed_test.py
# Author:       Wayne Stock
# Update:       2026-09-08
# Discription:  to check your internet speed 
#############################################

import speedtest

st = speedtest.Speedtest()
st.get_best_server()

print(f"Download: {st.download() / 1_000_000:.2f} Mbps")
print(f"Upload: {st.upload() / 1_000_000:.2f} Mbps")
print(f"Ping: {st.results.ping} ms")