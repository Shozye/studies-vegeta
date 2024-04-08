set Subjects;
set GroupSubjectIndexes;
set Activities;
set GroupActivityIndexes;
set ScheduleHours;
set Days;

param GroupsStartHours{GroupSubjectIndexes, Subjects};
param GroupsStartDays {GroupSubjectIndexes, Subjects};
param GroupTime {Subjects};
/* Parameters describing at what hour group start, at what day, and how long it takes */

param ActivityStartHours{GroupActivityIndexes, Activities};
param ActivityStartDays{GroupActivityIndexes, Activities};
param ActivityTime{Activities};
/* Parameters describing at what hour activity start, at what day, and how long it takes */

param Preferences{GroupSubjectIndexes, Subjects};
/* Preferences of liking groups */

var groupsPick{GroupSubjectIndexes, Subjects} binary;
var activitiesPick{GroupActivityIndexes, Activities} binary;
var schedule{Days, ScheduleHours} >= 0;

subject to group_pick{i in Subjects}:
    sum{j in GroupSubjectIndexes} groupsPick[j, i] = 1;
subject to activity_pick{i in Activities}:
    sum{j in GroupActivityIndexes} activitiesPick[j, i] = 1;
/* Students have to take one group from every activity and subject. */


subject to group_changes_schedule{i in Subjects, j in GroupSubjectIndexes}:
    if groupsPick[j, i] = 1 then
    sum{k in 0..(GroupTime[Subjects]-1)} schedule[GroupsStartDays[j, i], k+GroupsStartHours[j,i]];


var x >= 0;
minimize label: x;
solve;
end;