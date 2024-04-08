/* Mateusz Pełechaty, 261737 */
set Cities;
set Standards;
param Distances{Cities, Cities};
param Shortages{Cities, Standards};
param Surplus{Cities, Standards};
param CostsPerKm{Standards};

var send{Standards, Cities, Cities} >= 0;


subject to limit_send_to_surplus{c1 in Cities, standard in Standards}:
    sum{other in Cities} send[standard,c1,other] <= Surplus[c1, standard];
/* Any city, cannot send more than it's surplus */

subject to satiate_shortage_vip{c1 in Cities}:
    sum{other in Cities} send['VIP', other, c1] >= Shortages[c1, 'VIP'];
/* Vips must arrive to the city c1 */

subject to satiate_shortage_basic{c1 in Cities}:
    sum{other in Cities, standard in Standards} send[standard, other, c1] 
    >= 
    Shortages[c1, 'BASIC'] + Shortages[c1, 'VIP'];
/* BASIC and VIP camper arrivals must be more than basic and vip shortages. 
    It also allows VIPs to fill BASIC because they will 'move' through send 
    to the same city they are in. */

minimize cost:
    sum{c1 in Cities, c2 in Cities} 
    Distances[c1, c2]*(
        CostsPerKm['BASIC']*send['BASIC', c1, c2] 
        + CostsPerKm['VIP']*send['VIP', c1, c2]
    );


solve;
display cost;
display send;
end;
