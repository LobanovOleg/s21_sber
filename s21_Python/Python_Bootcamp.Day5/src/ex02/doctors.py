import threading
import random
import time


class Doctor(threading.Thread):
    def __init__(self, number, left, right):
        super().__init__()
        self.number = number
        self.left = left
        self.right = right

    def run(self):
        while True:
            time.sleep(random.random())
            if self.left.acquire(blocking=False) and self.right.acquire(blocking=False):
                print(f"Doctor {self.number}: BLAST!")
                self.left.release()
                self.right.release()
                break


def main():
    doctors = []
    screwdrivers = [threading.Lock() for _ in range(5)]

    for i in range(5):
        left = screwdrivers[i]
        right = screwdrivers[(i + 1) % 5]
        doctor = Doctor(i + 9, left, right)
        doctors.append(doctor)

    random.shuffle(doctors)

    for doctor in doctors:
        doctor.start()

    for doctor in doctors:
        doctor.join()


if __name__ == "__main__":
    main()
