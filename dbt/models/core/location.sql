{{ config(materialized="table") }}


select
    cast(country_code as string) as country_code,
    cast(latitude as float64) as latitude,
    cast(longitude as float64) as longitude,
    cast(country as string) as country_name
from {{ ref("world_country") }}
