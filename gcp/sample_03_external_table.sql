CREATE OR REPLACE EXTERNAL TABLE demo.Products_external_csv (
    ProductID STRING,
    ProductName STRING,
    Category STRING,
    Price INT64
)
OPTIONS (
    format = 'CSV',
    uris = ['gs://tir101-demo/demo_csv/*.csv'],
    skip_leading_rows = 1,
    max_bad_records = 1
);

select * from demo.Products_external_csv;

-----

CREATE EXTERNAL TABLE demo.Products_external_jsonl (
    ProductID INT64,
    ProductName STRING,
    Category STRING,
    Price NUMERIC
)
OPTIONS (
    format = 'NEWLINE_DELIMITED_JSON',
    uris = ['gs://tir101-demo/demo_jsonl/*.jsonl'],
    max_bad_records = 1
);

select * from demo.Products_external_jsonl;
