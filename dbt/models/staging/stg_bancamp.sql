{{ config(materialized="view") }}

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
    
    
from {{ source('bancamp', 'bancamp_sales_table') }}
{% if var('is_test_run', default=false) %}

  limit 100

{% endif %}