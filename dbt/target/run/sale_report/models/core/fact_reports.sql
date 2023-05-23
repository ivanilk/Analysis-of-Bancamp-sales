
  
    

    create or replace table `valued-watch-381913`.`dbt_sales_report`.`fact_reports`
    partition by timestamp_trunc(utc_date, day)
    
    OPTIONS()
    as (
       

select
    id,
    item_type,
    utc_date,
    bc.country_code ,
    slug_type,
    item_price,
    item_description,
    art_id,
    amount_paid_usd,
    artist_name,
    lc.latitude,
    lc.longitude,
    lc.country_name

from `valued-watch-381913`.`dbt_sales_report`.`stg_bancamp` as bc
inner join `valued-watch-381913`.`dbt_sales_report`.`location` as lc
on bc.country_code = lc.country_code
    );
  