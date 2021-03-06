import datetime


class Vehicle:

    def __init__(self, max_dist, capacity, charge_fast, charge_medium, charge_slow, start_time, end_time):
        self.max_dist = max_dist
        self.dist_left = self.max_dist
        self.capacity = capacity
        self.capacity_left = capacity
        self.charge_fast = charge_fast
        self.charge_medium = charge_medium
        self.charge_slow = charge_slow
        self.working_time = datetime.datetime.strptime(
            end_time, '%H:%M') - datetime.datetime.strptime(start_time, '%H:%M')
        self.working_time_left = self.working_time

    def consume_energy(self, dist):
        self.dist_left = self.dist_left - dist

    def consume_time(self, time):
        self.working_time_left = self.working_time_left - time

    def consume_capacity(self, capacity):
        self.capacity_left = self.capacity_left - capacity
