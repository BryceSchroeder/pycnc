import unittest
from pycnc import gcode_generator as gcg



class TestGenerateHeights(unittest.TestCase):
    def test_happy_path(self):
        count = 0
        for h in gcg.generate_heights(0.0, -8.0, -1.0):
            count +=1
        self.assertEqual(count,9)
        
    def test_wrong_direction(self):
        count=0
        gcg.generate_heights(0.0, -8.0, 1.0)
        self.assertRaises(gcg.WrongParameterError)

    
if __name__ == '__main__':
    unittest.main()
