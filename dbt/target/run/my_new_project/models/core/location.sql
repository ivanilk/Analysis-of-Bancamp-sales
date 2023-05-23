
  
    

    create or replace table `valued-watch-381913`.`dbt_sales_report`.`location`
    
    
    OPTIONS()
    as (
      


select
    cast(country_code as string) as country_code,
    cast(latitude as float64) as latitude,
    cast(longitude as float64) as longitude,
    cast(country as string) as country_name
from `valued-watch-381913`.`dbt_sales_report`.`location_lonandlat`
    );
  