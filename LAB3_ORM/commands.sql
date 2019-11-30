create index on cargo(barcode);
analyze;  //Query returned successfully in 324 msec.
explain (costs off) select * from cargo where barcode=831; -- 65msec Index Scan using cargo_worker_id_idx on cargo

explain (costs off) select * from cargo where worker_id>831;                                -- Seq Scan on cargo (actual time=0.009..1.353 rows=5000 loops=1)
                                                                                            -- Filter: (worker_id > 831)
                                                                                            -- Planning Time: 0.122 ms
                                                                                            -- Execution Time: 1.716 ms


create index on cargo(estimated_value); 196msec
explain (analyze, costs off) select barcode from cargo where worker_id>6283 and estimated_value = 600;
                                                                                            -- Bitmap Heap Scan on cargo (actual time=0.018..0.022 rows=4 loops=1)
                                                                                            -- Recheck Cond: (estimated_value = '600'::numeric)
                                                                                            -- Filter: (worker_id > 6283)
                                                                                            -- Rows Removed by Filter: 1
                                                                                            -- Heap Blocks: exact=5
                                                                                            --   ->  Bitmap Index Scan on cargo_estimated_value_idx (actual time=0.010..0.010 rows=5 loops=1)
                                                                                            -- Index Cond: (estimated_value = '600'::numeric)
                                                                                            -- Planning Time: 0.084 ms
                                                                                            -- Execution Time: 0.037 ms

--                                                                                             covering index
vacuum cargo;
select avg(worker_id) from cargo;
    explain (analyze, costs off) select barcode from cargo where worker_id>6283;
                                                                                            --   Index Scan using cargo_worker_id_idx on cargo (actual time=0.019..0.787 rows=2500 loops=1)
                                                                                            --   Index Cond: (worker_id > 6283)
                                                                                            --   Planning Time: 0.083 ms
                                                                                           --   Execution Time: 0.920 ms

create index on packing (packing_code, amount);
explain (analyze, costs off) select packing_code from packing where packing_code>831 and amount>10;
                                                                                            -- Index Only Scan using packing_packing_code_amount_idx on packing (actual time=0.426..0.426 rows=0 loops=1)
                                                                                            -- Index Cond: ((packing_code > 831) AND (amount > 10))
                                                                                            -- Heap Fetches: 0
                                                                                            -- Planning Time: 0.471 ms
                                                                                            -- Execution Time: 0.447 ms

explain (analyze, costs off) select packing_code from packing where packing_code>831 and weight>10;




explain (analyze, costs off) select full_name from client where lower(full_name)='anyrak'
                                                                                        -- Seq Scan on client (actual time=5.132..5.132 rows=0 loops=1)
                                                                                        --   Filter: (lower(full_name) = 'anyrak'::text)
                                                                                        --   Rows Removed by Filter: 5000
                                                                                        --   Planning Time: 2.179 ms
                                                                                        --   Execution Time: 5.552 ms
create index on client(lower(full_name));
explain (analyze, costs off) select full_name from client where lower(full_name)='anyrak'
                                                                                        -- Bitmap Heap Scan on client (actual time=0.023..0.023 rows=0 loops=1)
                                                                                        -- Recheck Cond: (lower(full_name) = 'anyrak'::text)
                                                                                        -- ->  Bitmap Index Scan on client_lower_idx (actual time=0.021..0.021 rows=0 loops=1)
                                                                                        -- Index Cond: (lower(full_name) = 'anyrak'::text)
                                                                                        -- Planning Time: 0.159 ms
                                                                                        -- Execution Time: 0.045 ms


-- select a.amname, p.name, pg_indexam_has_property(a.oid,p.name)
-- from pg_am a,
-- unnest(array['can_order','can_unique','can_multi_col','can_exclude']) p(name)
-- where a.amname = 'brin' order by a.amname;

-- properties of brin indexes


create table ts(doc text, doc_tsv tsvector);
insert into ts(doc) values
  ('Во поле береза стояла'),  ('Во поле кудрявая стояла'),
  ('Люли, люли, стояла'),     ('Люли, люли, стояла'),
  ('Некому березу заломати'), ('Некому кудряву заломати'),
  ('Люли, люли, заломати'),   ('Люли, люли, заломати'),
  ('Я пойду погуляю'),        ('Белую березу заломаю'),
  ('Люли, люли, заломаю'),    ('Люли, люли, заломаю');
set default_text_search_config = russian;
update ts set doc_tsv = to_tsvector(doc);
create index on ts using gin(doc_tsv);
select ctid, doc, doc_tsv from ts;-- number of page and position on the page
select (unnest(doc_tsv)).lexeme, count(*) from ts group by 1 order by 2 desc;  -- amount of each words in document


explain(analyze, costs off)
select doc from ts where doc_tsv @@ to_tsquery('стояла & кудрявая');
--                                                                     Bitmap Heap Scan on ts (actual time=0.043..0.043 rows=1 loops=1)
--                                                                     Recheck Cond: (doc_tsv @@ to_tsquery('стояла & кудрявая'::text))
--                                                                     Heap Blocks: exact=1
--                                                                     ->  Bitmap Index Scan on ts_doc_tsv_idx (actual time=0.033..0.033 rows=1 loops=1)
--                                                                     Index Cond: (doc_tsv @@ to_tsquery('стояла & кудрявая'::text))
--                                                                     Planning Time: 0.233 ms
--                                                                     Execution Time: 0.077 ms
select attname, correlation from pg_stats where tablename='cargo' order by correlation desc nulls last;
--create index on ref_client_worker using brin(time);
create index on cargo using brin(worker_id);


explain (costs off,analyze)
select *
from cargo
where worker_id > 1000 and worker_id <  1
                                                                    -- Index Scan using cargo_worker_id_idx on cargo (actual time=0.004..0.004 rows=0 loops=1)
                                                                    -- Index Cond: ((worker_id > 1000) AND (worker_id < 1))
                                                                    -- Planning Time: 0.177 ms
                                                                    -- Execution Time: 0.018 ms




CREATE OR REPLACE FUNCTION func() RETURNS trigger AS
$$BEGIN
   UPDATE "cargo" SET estimated_value = estimated_value - 10
      WHERE barcode = OLD.cargo_barcode;
   RETURN OLD;
END;$$ LANGUAGE plpgsql;

CREATE TRIGGER add_money
   BEFORE DELETE ON packing FOR EACH ROW
   EXECUTE PROCEDURE func();

select * from cargo where barcode = '26591'

    delete from packing where cargo_barcode = '26591'





CREATE OR REPLACE FUNCTION UPD()
RETURNS trigger AS
$$
begin
UPDATE client SET full_name = (SELECT REVERSE (n2.full_name) from client as n2 where (n2.client_number = client.client_number));
end;
$$ language plpgsql;

CREATE TRIGGER change_name
   BEFORE DELETE ON client FOR EACH ROW
   EXECUTE PROCEDURE func();


insert into client (full_name, client_number, client_type) values ('anyrak', '455678900987', 'sender')


select * from client where client_number = '455678900987';

delete from client where client_number = '455678900987';
CREATE OR REPLACE FUNCTION UPD()
RETURNS trigger AS
$$
begin
UPDATE client SET full_name = REVERSE (old.full_name);
return new;
end;
$$ language plpgsql;

CREATE TRIGGER change_name
   BEFORE DELETE ON client FOR EACH ROW
   EXECUTE PROCEDURE UPD();