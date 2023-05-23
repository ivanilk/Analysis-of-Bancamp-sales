{{ config(materialized='table') }}


select
    cast(country_code as nchar(2)) as country_code,
    cast(latitude as float) as latitude,
    cast(longitude as float) as longitude,
    cast(country as varchar(50)) as country_name
from {{ ref('location_lonandlat') }}