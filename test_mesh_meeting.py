import unittest
from datetime import datetime
from mesh_meeting import generate_time_slots
from mesh_meeting import (
    convert_to_datetime,
    generate_time_slots,
    populate_time_slots,
    calculate_matches,
    generate_meetings,
)


class MeshMeetingTests(unittest.TestCase):
    def test_convert_to_datetime(self):
        start_time, end_time = convert_to_datetime("Monday 9:00am-11:00am")
        self.assertEqual(start_time, datetime(1900, 1, 1, 9, 0))
        self.assertEqual(end_time, datetime(1900, 1, 1, 11, 0))

    def test_generate_time_slots(self):
        time_slots = generate_time_slots()
        start_time, end_time = convert_to_datetime("Monday 9:00am-5:00pm")
        part_start_time, part_end_time = convert_to_datetime("Friday 9:00am-12:00pm")
        print(time_slots.keys())
        chunks = int((end_time - start_time).total_seconds() / (15 * 60)) * 4
        chunks += int((part_end_time - part_start_time).total_seconds() / (15 * 60))
        self.assertEqual(len(time_slots), chunks)

    def test_populate_time_slots(self):
        time_slots = {
            "Monday 9:00am-9:15am": set(),
            "Monday 9:15am-9:30am": set(),
            "Monday 9:30am-9:45am": set(),
            # ...
        }
        schedule = {
            "john.doe@example.com": {
                "name": "John Doe",
                "availability": ["Monday 9:00am-11:00am"],
            },
            "jane.doe@example.com": {
                "name": "Jane Doe",
                "availability": ["Monday 10:00am-12:00pm"],
            },
        }
        updated_time_slots = populate_time_slots(time_slots, schedule)
        self.assertEqual(
            updated_time_slots["Monday 9:00am-9:15am"], {"john.doe@example.com"}
        )
        self.assertEqual(
            updated_time_slots["Monday 10:00am-10:15am"], {"jane.doe@example.com"}
        )

    def test_calculate_matches(self):
        time_slots = {
            "Monday 9:00am-9:15am": {"john.doe@example.com", "jane.doe@example.com"},
            "Monday 9:15am-9:30am": {"john.doe@example.com"},
            "Monday 9:30am-9:45am": {"jane.doe@example.com"},
            # ...
        }
        matches = calculate_matches(time_slots)
        self.assertEqual(matches, ["Monday 9:00am-9:15am"])

    def test_generate_meetings(self):
        potential_matches = ["Monday 9:00am-9:15am", "Monday 9:15am-9:30am"]
        meetings = generate_meetings(potential_matches)
        self.assertEqual(len(meetings), 2)  # Two meetings generated


if __name__ == "__main__":
    unittest.main()
