

  create or replace view `valued-watch-381913`.`dbt_sales_report`.`stg_bancamp`
  OPTIONS()
  as 

select
    _id as id
    
from `valued-watch-381913`.`bancamp_sales_ds`.`bancamp_sales_table`
;

