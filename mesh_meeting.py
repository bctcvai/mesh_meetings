import argparse
import os
import random
import shutil
import sys
import yaml

from collections import defaultdict
from datetime import datetime, timedelta
from pprint import pprint

import vobject
from dateutil.relativedelta import MO, relativedelta

"""
This script is used to schedule Mesh Meetings™ between participants based on their availability.

The script works as follows:

1. It first sets up the names and emails of all participants.
2. It then defines the availability of each participant in terms of time ranges on specific days of the week.
3. The script converts these time ranges into datetime objects for easier manipulation.
4. It generates a vCalendar (vCal) file for a meeting between two people. The vCal file includes the start and end times of the meeting and the attendees.
5. The script generates a list of time slots for the week, from Monday 9:00am to Friday 12pm.

The output of the script is a set of vCal files, one for each scheduled meeting, which can be imported into a calendar application.

Note: The script assumes that all times are in the same timezone.

Example usage:
$> python mesh_meeting.py schedule.yaml output

Where schedule.yaml looks like:
john.doe@example.com:
  name: John Doe
  availability: 
    - Monday 9:00am-11:00am
    - Tuesday 10:00am-12:00pm
    - Wednesday 1:00pm-3:00pm
    - Thursday 2:00pm-4:00pm
jane.doe@example.com:
  name: Jane Doe
  availability: 
    - Monday 1:00pm-3:00pm
    - Tuesday 2:00pm-4:00pm
    - Wednesday 9:00am-11:00am
    - Thursday 10:00am-12:00pm
robert.smith@example.com:
  name: Robert Smith
  availability: 
    - Monday 2:00pm-4:00pm
    - Tuesday 9:00am-11:00am
    - Wednesday 10:00am-12:00pm
    - Thursday 1:00pm-3:00pm
"""

# Convert time range to datetime object
# Monday 9:00am-11:00am -> (datetime(2020, 9, 14, 9, 0), datetime(2020, 9, 14, 11, 0))
def convert_to_datetime(time_range):
    day, start_time_end_time_str = time_range.split()
    start_time, end_time = start_time_end_time_str.split('-')
    day_index = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
    start_datetime = datetime.strptime(f"{day_index[day]} {start_time}", "%w %I:%M%p")
    end_datetime = datetime.strptime(f"{day_index[day]} {end_time}", "%w %I:%M%p")
    start_datetime += timedelta(days=day_index[day])
    end_datetime += timedelta(days=day_index[day])
    return start_datetime, end_datetime

def make_vcal(schedule, p0, p1, meet_time, end_time):
    """
    Create a vCalendar object for a mesh meeting between two participants.

    Args:
        schedule (dict): A dictionary containing the schedule information of participants.
        p0 (str): The identifier of the first participant.
        p1 (str): The identifier of the second participant.
        meet_time (datetime): The start time of the meeting.
        end_time (datetime): The end time of the meeting.

    Returns:
        vobject.iCalendar: The vCalendar object representing the mesh meeting.
    """
    cal = vobject.iCalendar()
    event = cal.add('vevent')

    event.add('summary').value = f'Mesh Meeting™ {schedule[p0]['name']}/{schedule[p1]['name']}'
    event.add('dtstart').value = meet_time
    event.add('dtend').value = end_time

    attendee = event.add('attendee')
    attendee.value = f'mailto:{p0}'

    attendee = event.add('attendee')
    attendee.value = f'mailto:{p1}'

    return cal

def generate_time_slots():
    """
    Generate time slots for meetings.

    Returns:
        dict: A dictionary containing time slots as keys and an empty set as values.
    """
    time_slots = {}
    start_time = datetime.strptime("Monday 9:00am", "%A %I:%M%p")
    end_time = start_time + timedelta(days=4) + timedelta(hours=3)
    current_time = start_time
    while current_time < end_time:
        meeting_end_time = current_time + timedelta(minutes=15)
        if (current_time.hour < 17 and current_time.hour >= 9):
            time_slots[f"{current_time.strftime('%A %I:%M%p')}-{meeting_end_time.strftime('%I:%M%p')}"] = set()
        current_time = meeting_end_time
    return time_slots

def populate_time_slots(time_slots, schedule):
    """
    Populates the time slots with people's availability based on the given schedule.

    Args:
        time_slots (dict): A dictionary representing the time slots.
        schedule (dict): A dictionary representing the schedule of people's availability.

    Returns:
        dict: A dictionary representing the updated time slots with people's availability.
    """
    # Convert to people availability format
    people_availability = {}
    for person, person_schedule in schedule.items():
        people_availability[person] = person_schedule['availability']
    for person, availability in people_availability.items():
        for slot in time_slots:
            slot_start, slot_end = convert_to_datetime(slot)
            for time_range in availability:
                avail_start, avail_end = convert_to_datetime(time_range)
                if slot_start < avail_end and slot_end > avail_start:
                    time_slots[slot].add(person)
    return time_slots


def calculate_matches(time_slots):
    """
    Calculate the matches by identifying the time slots with more than one person.

    Args:
        time_slots (dict): A dictionary containing time slots as keys and a list of people as values.

    Returns:
        list: A list of time slots with more than one person.
    """
    potential_matches = []
    for slot, people in time_slots.items():
        if len(people) > 1:
            potential_matches.append(slot)
    return potential_matches

def generate_meetings(potential_matches):
    """
    Generate meetings between potential matches.

    Args:
        potential_matches (list): A list of potential matches.

    Returns:
        dict: A dictionary representing the generated meetings, where the keys are people and the values are the matches.
    """

    # TODO: This is a very basic matching algorithm and could be improved.
    meetings = defaultdict(lambda: {})
    random.shuffle(potential_matches)

    max_meetings_per_person = 3
    max_meeting_per_match = 1
    match_count = defaultdict(lambda: 0)

    for k in potential_matches:
        people = list(time_slots[k])
        random.shuffle(people)
        p0 = people[0]
        p1 = people[1]
        abc = [p0, p1]
        abc.sort()
        if len(meetings[p0]) < max_meetings_per_person and len(meetings[p1]) < max_meetings_per_person and match_count[f"{abc[0]}_{abc[1]}"] == 0:
            meetings[p0][k] = p1
            meetings[p1][k] = p0
            match_count[f"{abc[0]}_{abc[1]}"] += 1
        else:
            random.shuffle(people)
            p0 = people[0]
            p1 = people[1]
            abc = [p0, p1]
            abc.sort()
            if len(meetings[p0]) < max_meetings_per_person and len(meetings[p1]) < max_meetings_per_person and match_count[f"{abc[0]}_{abc[1]}"] == 0:
                meetings[p0][k] = p1
                meetings[p1][k] = p0
                match_count[f"{abc[0]}_{abc[1]}"] += 1
    return meetings

def generate_vcal_files(meetings, schedule, relative_week, absolute_monday):
    """
    Generate vCal files for mesh meetings.

    Args:
        meetings (dict): A dictionary containing the meetings data.
        schedule (dict): A dictionary containing the schedule data.
        relative_week (int): The relative week number.
        absolute_monday (datetime): The absolute Monday date.

    Returns:
        dict: A dictionary containing the vCal files grouped by user.
    """
    vcal_registry = {}
    vcal_by_user = defaultdict(lambda: [])

    if absolute_monday:
        last_monday = absolute_monday
    else:
        last_monday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + relativedelta(weekday=MO(relative_week))

    print(f"For week of {last_monday}")

    print(f"=== Mesh Meetings™ === ")
    for p0, meetings in meetings.items():
        print(p0)
        for meet_time, p1 in meetings.items():
            print(f"\t{meet_time}: {p1}")
            abc = [p0, p1]
            abc.sort()
            key = f"{abc[0]}_{abc[1]}"
            if key not in vcal_registry:
                slot_start, slot_end = convert_to_datetime(meet_time)
                abs_start_meet_time = (slot_start - datetime(1900, 1, 1)) + last_monday
                abs_end_meet_time = (slot_end - datetime(1900, 1, 1)) + last_monday
                vcal_registry[key] = make_vcal(schedule, abc[0], abc[1], abs_start_meet_time, abs_end_meet_time)
                vcal_by_user[abc[0]].append(vcal_registry[key])
                vcal_by_user[abc[1]].append(vcal_registry[key])

    return vcal_by_user

def save_vcal_files(vcal_by_user, schedule):
    """
    Save vCal files for each user in the given schedule.

    Args:
        vcal_by_user (dict): A dictionary containing vCal files for each user.
        schedule (dict): A dictionary containing the schedule information.

    Returns:
        None
    """
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output", exist_ok=True)
    for p0, vcal_files in vcal_by_user.items():
        for idx, mesh_invite in enumerate(vcal_files):
            with open(f"output/{schedule[p0]['name']}_{idx}.vcs", "w") as f:
                f.write(mesh_invite.serialize())

# Main function
# Generates meetings between people
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Mesh Meetings™')
    parser.add_argument("--relative-week", type=int, help="Week relative to current week, defaults to auto")
    parser.add_argument("--absolute-week", type=str, help='Week in YYYY-MM-DD format, overrides relative week')
    parser.add_argument('schedule', type=str, help='Path to schedule file')
    parser.add_argument('output', type=str, help='Path to output directory')
    args = parser.parse_args()

    # This code block determines the relative or absolute week for generating mesh meetings. 
    # If the `--relative-week` argument is not provided, it automatically determines the week based on the current date. 
    # If the `--absolute-week` argument is provided, it calculates the Monday of that specific week. 
    # The result is stored in the `relative_week` and `absolute_monday` variables for further use in the script.
    relative_week = args.relative_week
    # If we are in auto mode
    if relative_week is None: 
        if datetime.now().weekday() > 0:
            relative_week = 0
        else:
            relative_week = -1

    absolute_monday = None
    if args.absolute_week is not None:
        absolute_week = datetime.strptime(args.absolute_week, "%Y-%m-%d")
        that_monday = absolute_week + relativedelta(weekday=MO(-1))
        absolute_monday = that_monday# Convert to the monday of that week
        print(f"Absolute Mode: Week of {args.absolute_week} Monday is {absolute_monday}")
    else:
        last_monday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + relativedelta(weekday=MO(relative_week))
        print(f"Relative Mode: Week of {relative_week} is {last_monday}")

    with open(args.schedule) as fp:
     schedule = yaml.safe_load(fp)

    time_slots = generate_time_slots()
    time_slots = populate_time_slots(time_slots, schedule)
    potential_matches = calculate_matches(time_slots)
    meetings = generate_meetings(potential_matches)
    vcal_by_user = generate_vcal_files(meetings, schedule, relative_week, absolute_monday)
    save_vcal_files(vcal_by_user, schedule)
