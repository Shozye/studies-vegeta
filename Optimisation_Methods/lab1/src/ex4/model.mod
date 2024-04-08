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

subject to group_pick{s in Subjects}:
    sum{g in GroupSubjectIndexes} groupsPick[g, s] = 1;
subject to activity_pick{a in Activities}:
    sum{g in GroupActivityIndexes} activitiesPick[g, a] = 1;
/* Students have to take one group from every activity and subject. */

subject to group_changes_schedule{day in Days, hours in ScheduleHours}:
    sum{g in GroupSubjectIndexes, s in Subjects}(
        if ( 
            GroupsStartDays[g, s] = day 
            and GroupsStartHours[g,s] <= hours 
            and hours < GroupsStartHours[g,s] + GroupTime[s]
        ) then
            groupsPick[g,s]
    ) 
    + 
    sum{g in GroupActivityIndexes, a in Activities}(
        if ( ActivityStartDays[g, a] = day 
            and ActivityStartHours[g,a] <= hours 
            and hours < ActivityStartHours[g,a] + ActivityTime[a]
         ) then
        activitiesPick[g, a]
    ) 
    <= 1;
/* We calculate how many groups and activities there are at certain time by summing through all groups and activities 
    And do not allow multitasking by forcing it to be not more than 1 */

subject to do_not_overload{day in Days}:
    sum{g in GroupSubjectIndexes, s in Subjects}(
        if GroupsStartDays[g, s] = day then
            GroupTime[s] * groupsPick[g, s]
    ) <= 8;
/* Do not allow for overloading of student by signing him on more than 4 hours of exercises */

subject to high_expectations{g in GroupSubjectIndexes, s in Subjects}: 
        if Preferences[g, s] < 5 then groupsPick[g,s] = 0;

subject to no_wed_fri:
    sum{g in GroupSubjectIndexes, s in Subjects}
        if GroupsStartDays[g,s] = 3 or GroupsStartDays[g,s]=5 then
            groupsPick[g,s]
    = 0;
    

maximize total_preference: 
    sum{g in GroupSubjectIndexes, s in Subjects}
        groupsPick[g, s] * Preferences[g, s];
    
/* Total preference is the just sum over all group picks to get their preferences */

solve;
display total_preference;
display groupsPick;
end;
