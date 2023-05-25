{{ config(materialized='table',
    partition_by={
        "field": "utc_date",
        "data_type": "timestamp",
        "granularity": "day"
    }
)}} 

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

from {{ ref('stg_bancamp') }} as bc
inner join {{ ref('location') }} as lc
on bc.country_code = lc.country_code
