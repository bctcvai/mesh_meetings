# Mesh Meeting Scheduler

This Python script is used to schedule Mesh Meetings™ between participants based on their availability.

## How it works

1. It first sets up the names and emails of all participants.
2. It then defines the availability of each participant in terms of time ranges on specific days of the week.
3. The script converts these time ranges into datetime objects for easier manipulation.
4. It generates a vCalendar (vCal) file for a meeting between two people. The vCal file includes the start and end times of the meeting and the attendees.
5. The script generates a list of time slots for the week, from Monday 9:00am to Friday 12pm.

The output of the script is a set of vCal files, one for each scheduled meeting, which can be imported into a calendar application.

## Usage

```shell
$> python mesh_meeting.py schedule.yaml output
```
Where schedule.yaml looks like:
```yaml
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
```

The output is the directory where the vCal files will be saved.

### Example Schedule



## License
This project is licensed under the BSD 3-Clause License. See the LICENSE file for details.