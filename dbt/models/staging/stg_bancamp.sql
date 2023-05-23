{{ config(materialized="view") }}

select
    _id as id
    
from {{ source('bancamp', 'bancamp_sales_table') }}
{% if var('is_test_run', default=false) %}

  limit 100

{% endif %}