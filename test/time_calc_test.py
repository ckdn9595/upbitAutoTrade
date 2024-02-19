import unittest
import datetime


# 날짜 및 시간 객체 간의 차이 계산
# delta = datetime.datetime(2022, 3, 1, 12, 30, 45) - datetime.datetime(2022, 2, 28, 11, 15, 30)
# print("두 날짜 및 시간의 차이:", delta)

class DateCalcTest(unittest.TestCase):

    
    def test_날짜파싱테스트(self):
        str_date = "2022-03-01 12:30:45"
        dt = datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
        
        str_date2 = "20220301123045"
        dt2 = datetime.datetime.strptime(str_date2, "%Y%m%d%H%M%S")
        self.assertEqual(dt, dt2)
        
    
    def test_시작일종료일입력시분구하기(self):
        str_date1 = "20220301123045"
        start = datetime.datetime.strptime(str_date1, "%Y%m%d%H%M%S")
        
        str_date2 = "20220301123145"
        end = datetime.datetime.strptime(str_date2, "%Y%m%d%H%M%S")
        
        diff = end - start
        
        self.assertIsInstance(diff,  datetime.timedelta)
        self.assertEqual(diff.seconds/60,1)
        
if __name__ == '__main__':
    unittest.main()