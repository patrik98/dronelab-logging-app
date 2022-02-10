import unittest
from app_utils import SessionID

class TestSessionIDMethods(unittest.TestCase):

    def test_get_date(self):
        sess = SessionID()
        sess.create_sess_id(date="20220901", sess_num="2")
        self.assertEqual("20220901", sess.get_date())

    def test_get_sess_num(self):
        sess = SessionID()
        sess.create_sess_id(date="20220901", sess_num="2")
        self.assertEqual("2", sess.get_sess_num())

    def test_wrong_input(self):
        with self.assertRaises(ValueError):
            sess = SessionID()
            sess.create_sess_id("asdfgg", sess_num="2")

    def test_get_following_id(self):
        sess = SessionID()
        sess.create_sess_id(date="20220901", sess_num="2")
        self.assertEqual(SessionID("202209013"), sess.get_following_id())

    def test_equal(self):
        sess = SessionID()
        sess.create_sess_id(date="20220901", sess_num="2")
        sess2 = SessionID()
        sess2.create_sess_id(date="20220901", sess_num="2")
        self.assertTrue(sess == sess2)

    def test_lt(self):
        sess = SessionID()
        sess.create_sess_id(date="20220901", sess_num="2")
        sess2 = SessionID()
        sess2.create_sess_id(date="20220901", sess_num="3")
        self.assertTrue(sess < sess2)
        sess2 = SessionID()
        sess2.create_sess_id(date="20220801", sess_num="3")
        self.assertTrue(sess > sess2)


if __name__ == '__main__':
    unittest.main()
