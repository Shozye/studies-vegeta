/* Mateusz Pełechaty, 261737 */
set ProductIndexes;
set ResourceIndexes;
set FirstClassProductIndexes;
set SecondClassProductIndexes;

param ResourceMinBuy{ResourceIndexes};
param ResourceMaxBuy{ResourceIndexes};
param ResourceCostBuy{ResourceIndexes};

param ProductValue{ProductIndexes};

param WasteCosts{ResourceIndexes, FirstClassProductIndexes};
param WasteCreation{ResourceIndexes, FirstClassProductIndexes}; 

param MixNotBiggerThanConstraint{ResourceIndexes, ProductIndexes};
param MixNotSmallerThanConstraint{ResourceIndexes, ProductIndexes};

var res_buy{ResourceIndexes} >= 0;
/* How much resource should i buy of every type*/
var r_to_prod{ResourceIndexes, ProductIndexes} >= 0;
/* Array var telling how many of each resource went into first class products */
var mixes{ProductIndexes} >= 0;
/* total masses of products for any product */
var wastes{ResourceIndexes, FirstClassProductIndexes} >= 0;
/* Wastes total. Indeed wastes[i,j] = utilizated_wastes[i,j] + used_wastes[i,j]*/
var utilizated_wastes{ResourceIndexes, FirstClassProductIndexes} >= 0;
/* Wastes that were utilizated in the end */
var used_wastes{ResourceIndexes, FirstClassProductIndexes} >= 0;
/* Those are wastes that were used to produce second class products */
var products{ProductIndexes} >= 0;
/* Variables describing how many kg of each product was created*/

var how_much_money_acquired >= 0;
var how_much_money_utilization_spent >= 0;
var how_much_money_to_buy >= 0;



subject to buy_constraints{i in ResourceIndexes}: 
    ResourceMinBuy[i] <= res_buy[i] <= ResourceMaxBuy[i];
/* MinBuy and MaxBuy due to contracts */

subject to resource_division{i in ResourceIndexes}:
    res_buy[i] = sum {j in ProductIndexes} r_to_prod[i, j];

subject to mix_product{i in FirstClassProductIndexes}: 
    mixes[i] = (sum{j in ResourceIndexes} r_to_prod[j, i]);

subject to mix_second_class_product{i in SecondClassProductIndexes}:
    mixes[i] = r_to_prod[i-2, i] + sum{j in ResourceIndexes}(used_wastes[j, i-2]);
/* Ingredient mixes to create product */

subject to waste_division{i in ResourceIndexes, j in FirstClassProductIndexes}:
    wastes[i,j] = utilizated_wastes[i,j] + used_wastes[i,j];
/* dividing wastes into was to utilizate and to use in production */

subject to resource_not_smaller_than_in_mix{i in ResourceIndexes, j in ProductIndexes}:
    r_to_prod[i,j] >= MixNotSmallerThanConstraint[i,j] * mixes[j];

subject to resource_not_bigger_than_in_mix{i in ResourceIndexes, j in ProductIndexes}:
    r_to_prod[i,j] <= MixNotBiggerThanConstraint[i,j] * mixes[j];
/* Constraints in all production lines about amount of resource to product */

subject to production_first_class_items{i in FirstClassProductIndexes}: 
    mixes[i] = products[i] + sum{j in ResourceIndexes} wastes[j, i];
/* Production of First Class items - Division between product and wastes */

subject to waste_creation{i in ResourceIndexes, j in FirstClassProductIndexes}:
    wastes[i,j] = r_to_prod[i,j]*WasteCreation[i,j];
/*Creation of wastes from products 1,2 */

subject to production_second_class_items{i in SecondClassProductIndexes}:
    products[i] = mixes[i];
/* All that mixed has combined into product. */


subject to utilization: 
    how_much_money_utilization_spent = sum{i in ResourceIndexes, j in FirstClassProductIndexes} 
        utilizated_wastes[i, j] * WasteCosts[i,j];

subject to selling_products:
    how_much_money_acquired = sum{i in ProductIndexes} products[i]*ProductValue[i];

subject to buy_products:
    how_much_money_to_buy = sum{i in ResourceIndexes} res_buy[i]*ResourceCostBuy[i];

maximize profit: how_much_money_acquired - how_much_money_utilization_spent - how_much_money_to_buy;

solve;
display how_much_money_acquired;
display how_much_money_utilization_spent;
display how_much_money_to_buy;
display res_buy;
display products;
display profit;

display wastes;
display utilizated_wastes;
display used_wastes;
display r_to_prod;

end;
