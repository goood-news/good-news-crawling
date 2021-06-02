import unittest
from cleansing import contents_cleansing


class Test_Sample01(unittest.TestCase):
  test_case = [
    "<p>웬디 셔먼 미국 국무부 부장관이 2일 미국 정부가 북한과 대화할 준비가 돼 있다고 말했다.</p>",
    "<span>글씨크기 조절하기</span>",
    "<p>(서울=연합뉴스) 노재현 송상호 기자 = 웬디 셔먼 미국 국무부 부장관이 2일 미국 정부가 북한과 대화할 준비가 돼 있다고 말했다.</p>",
    "<span class='ico_news'>바로가기 링크 더보기/접기</span>",
    "<script src='//t1.daumcdn.net/harmony_static/cloud/2021/06/01/vendor.060f681fd55112aaf724.js'></script>"
  ]

  def test_sample(self):
    self.assertTrue(7==(2+5))

  # def test_cleansing(self):
  #   self.assertEqual(contents_cleansing("<p>웬디 셔먼 미국 국무부 부장관이 2일 미국 정부가 북한과 대화할 준비가 돼 있다고 말했다.</p>")==">웬디 셔먼 미국 국무부 부장관이 2일 미국 정부가 북한과 대화할 준비가 돼 있다고 말했다.")



if __name__ == '__main__': 
  unittest.main()