import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_user_workflow(self):
        at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=30)
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.metric[0].value, '15')
        at.text_input[0].set_value('Juan Pablo Osorio')
        at.text_input[1].set_value('555-0101')
        at.text_input[2].set_value('juan@example.com')
        at.button[0].click().run()
        self.assertEqual(at.metric[0].value, '16')
        at.text_input[3].set_value(' juan pablo osorio ')
        at.button[1].click().run()
        self.assertEqual(at.table[0].value.iloc[0]['name'], 'Juan Pablo Osorio')
        at.button[-1].click().run(timeout=30)
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state['comparison']['contacts'], 16)
        at.text_input[4].set_value('Juan Pablo Osorio')
        at.checkbox[0].check()
        at.button[2].click().run()
        self.assertEqual(at.metric[0].value, '15')
        self.assertIsNone(at.session_state['tree'].search('Juan Pablo Osorio'))
        self.assertEqual(len(at.exception), 0)
