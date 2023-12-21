# Mesh Meeting Scheduler

This repository is used to schedule Mesh Meetings™ between participants based on their availability.

## What is a Mesh Meeting?

A Mesh Meeting™ is built upon the idea of increasing collaboration and communication through intentionally scheduled but unstructured 15 minute meetings. The concept can be used in geographically diverse remote teams, but may also provide value to in-person teams. A twist on the idea of "getting everyone in the same room", this scheduling tactic matches pairs of people based on their availability over the course of time.

Through short scheduled meetings team members can collaborate, socialize, or otherwise uncover roadblocks not addressed in traditional team meetings. Depending on the depth of the team in the mesh, the meetings can also serve as brief mentoring opportunities up and down the leadership ranks. Additional breadth to the mesh can provide learning opportunities for mesh members who may interact with someone they may not have organically.

## How it works

1. Setup a schedule.yaml file for the mesh participants.
2. It  defines the emails, names, and availability of each participant in terms of time ranges on specific days of the week.
3. The script extrapolates each availability segment into the full business week, in 15 minute intervals. This range is assumed to be 9am Monday to 12pm on Friday.
4. In addition to a text output of all proposed meetings, it generates a vCalendar (vCal) file for a meeting between two people. The vCal file includes the start and end times of the meeting and the attendees.

The output of the script is a set of vCal files, one for each scheduled meeting, which can be imported into a calendar application.

## Usage

```shell
python mesh_meeting.py schedule.yaml output
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
