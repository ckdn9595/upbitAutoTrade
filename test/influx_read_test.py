import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import matplotlib.pyplot as plt
import pytz
from influx_read import readInfluxData
from datetime import datetime, timezone, time, timedelta

timezone = pytz.timezone("Asia/Seoul")

influx_reader = readInfluxData()
start_str = "2023-12-02 09:00"
end_str = "2023-12-02 09:05"
start = datetime.strptime(
    start_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone).isoformat()
end = datetime.strptime(
    end_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone).isoformat()
json_data = influx_reader.read_with_range("KRW-BTC", start, end)
print(json_data)
# class InfluxReadTest(unittest.TestCase):
#     def test_날짜간격으로읽어오기(self):
#         influx_reader = readInfluxData()
#         start_str = "2023-12-02 09:00"
#         end_str = "2023-12-02 09:05"
#         start = datetime.strptime(
#             start_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone).isoformat()
#         end = datetime.strptime(
#             end_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone).isoformat()
#         json_data = influx_reader.read_with_range("KRW-BTC", start, end)
#         self.assertTrue(json_data, "json_data should not be empty.")
#         self.assertIn('close', json_data,"json_data should contain 'expected_key'.")

#     def test_지난N일로읽어오기(self):
#         self.assertTrue(True)


# if __name__ == '__main__':
#     unittest.main()
