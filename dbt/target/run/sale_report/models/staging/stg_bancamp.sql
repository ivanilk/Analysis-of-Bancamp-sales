

  create or replace view `valued-watch-381913`.`dbt_sales_report`.`stg_bancamp`
  OPTIONS()
  as 

select
    _id as id,
    item_type,
    utc_date,
    country_code,
    slug_type,
    item_price,
    item_description,
    art_id,
    amount_paid_usd,
    releases,
    artist_name,
    
    
from `valued-watch-381913`.`bancamp_sales_ds`.`bancamp_sales_table`
;

