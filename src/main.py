from rotator import Rotator
import sys

if __name__ == '__main__':
    rotator = Rotator(sys.argv)
    rotator.init()
    sys.exit(rotator.exec())